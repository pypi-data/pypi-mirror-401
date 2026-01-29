import asyncio
from sxd_core import io
import os
import shutil
import tarfile
from pathlib import Path
from typing import Dict, List, Optional

import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile, Depends, Security, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel

from sxd_core.auth import get_auth_manager, User
from .build import BuildEngine
from .trigger import TriggerRule, TriggerService

app = FastAPI(title="SXD Master Service")
build_engine = BuildEngine()
trigger_service = TriggerService()

# --- Auth Dependency ---

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def get_current_user(api_key: str = Security(api_key_header)) -> User:
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key",
        )

    auth = get_auth_manager()
    user = auth.authenticate(api_key)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    return user


# --- Models for Upload API ---


class FileInfo(BaseModel):
    path: str
    size: int


class UploadInitRequest(BaseModel):
    customer_id: str
    files: List[FileInfo]


class NodeAssignment(BaseModel):
    url: str
    files: List[str]
    total_bytes: int


class UploadInitResponse(BaseModel):
    session_id: str
    assignments: Dict[str, NodeAssignment]
    total_files: int
    total_bytes: int
    upload_token: str


class UploadStatus(BaseModel):
    session_id: str
    status: str
    customer_id: str
    files_received: int
    total_files: int
    bytes_received: int
    total_bytes: int
    episode_id: Optional[str] = None
    error: Optional[str] = None


# --- Upload Endpoints (Direct-to-Worker Architecture) ---


def _get_available_workers() -> List[str]:
    """Get list of available worker nodes from environment or discovery."""
    workers_env = os.getenv("SXD_WORKER_NODES", "")
    if workers_env:
        return [w.strip() for w in workers_env.split(",") if w.strip()]

    # Fallback: try to discover from ClickHouse node_metrics
    try:
        from sxd_core.clickhouse import ClickHouseManager

        ch = ClickHouseManager()
        result = ch.execute_query(
            "SELECT DISTINCT node FROM sxd.node_metrics "
            "WHERE timestamp > now() - INTERVAL 5 MINUTE"
        )
        return [r["node"] for r in result] if result else []
    except Exception:
        return []


@app.post("/api/upload/init", response_model=UploadInitResponse)
async def init_upload(
    request: UploadInitRequest, user: User = Depends(get_current_user)
):
    """
    Initialize upload session with load-balanced file distribution.

    Master assigns each file to optimal worker node based on current load.
    Files are uploaded directly to workers - no data flows through master.
    """
    from sxd_core.ops.node_metrics import compute_file_assignments

    session_id = f"sess-{io.uuid4().replace('-', '')[:12]}"
    worker_nodes = _get_available_workers()

    if not worker_nodes:
        raise HTTPException(
            status_code=503,
            detail="No worker nodes available. Configure SXD_WORKER_NODES or check node metrics.",
        )

    # Check permission
    auth = get_auth_manager()
    if not auth.check_permission(user, "job", "submit", request.customer_id):
        raise HTTPException(
            status_code=403,
            detail=f"Permission denied for customer {request.customer_id}",
        )

    # Prepare file list for assignment
    files_for_assignment = [{"path": f.path, "size": f.size} for f in request.files]

    # Compute load-balanced assignments
    worker_port = int(os.getenv("SXD_WORKER_UPLOAD_PORT", "8081"))
    allocations = compute_file_assignments(
        files=files_for_assignment,
        available_nodes=worker_nodes,
        worker_port=worker_port,
    )

    # Generate signed upload token
    # Valid for 24 hours (86400s) to allow for large uploads/pauses
    token = auth.create_upload_token(session_id, request.customer_id, ttl=86400)

    total_bytes = sum(f.size for f in request.files)

    # Build response format and node_assignments for ClickHouse
    assignments: Dict[str, NodeAssignment] = {}
    node_assignments_json: Dict[str, dict] = {}

    for node, alloc in allocations.items():
        assignments[node] = NodeAssignment(
            url=alloc.url,
            files=alloc.files,
            total_bytes=alloc.total_bytes,
        )
        node_assignments_json[node] = {
            "url": alloc.url,
            "files": alloc.files,
            "total_bytes": alloc.total_bytes,
        }

    # Start the UploadCoordinatorWorkflow
    # This acts as the state manager for the session
    from sxd_core.config import get_temporal_config

    try:
        from temporalio.client import Client

        tc = get_temporal_config()
        client = await Client.connect(f"{tc['host']}:{tc['port']}")

        await client.start_workflow(
            "upload-coordinator",
            args=[
                {
                    "session_id": session_id,
                    "customer_id": request.customer_id,
                    "files": files_for_assignment,
                    "worker_nodes": worker_nodes,
                }
            ],
            id=session_id,
            task_queue="default",
        )
    except Exception as e:
        print(f"Failed to start upload-coordinator: {e}")
        # Graceful degradation: CLI gets assignments regardless; workflow tracks completion.

    return UploadInitResponse(
        session_id=session_id,
        assignments=assignments,
        total_files=len(request.files),
        total_bytes=total_bytes,
        upload_token=token,
    )


@app.post("/api/upload/{session_id}/complete")
async def complete_session(session_id: str, user: User = Depends(get_current_user)):
    """
    Signal the UploadCoordinatorWorkflow to finalize the upload.
    """
    from sxd_core.clickhouse import ClickHouseManager
    from sxd_core.config import get_temporal_config

    # Update ClickHouse state for immediate CLI feedback
    # (The workflow will also update its state eventually)
    ch = ClickHouseManager()

    # Signal the workflow
    try:
        from temporalio.client import Client

        tc = get_temporal_config()
        client = await Client.connect(f"{tc['host']}:{tc['port']}")

        handle = client.get_workflow_handle(session_id)
        await handle.signal("complete_upload")

        # We can update CH here optimistically to "PROCESSING"
        episode_id = f"ep-{session_id[5:]}"
        ch.update_upload_session(session_id, status="PROCESSING", episode_id=episode_id)

        return {
            "session_id": session_id,
            "status": "processing",
            "message": "Signal sent to upload-coordinator",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to signal workflow: {e}")


@app.get("/api/upload/{session_id}/status", response_model=UploadStatus)
async def get_upload_status(session_id: str, user: User = Depends(get_current_user)):
    """Get the status of an upload session from ClickHouse."""
    from sxd_core.clickhouse import ClickHouseManager

    ch = ClickHouseManager()
    session = ch.get_upload_session(session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return UploadStatus(
        session_id=session_id,
        status=session["status"],
        customer_id=session["customer_id"],
        files_received=session["files_received"],
        total_files=session["total_files"],
        bytes_received=session["bytes_received"],
        total_bytes=session["total_bytes"],
        episode_id=session.get("episode_id"),
        error=session.get("error"),
    )


@app.get("/api/upload/{session_id}/resume")
async def get_resume_info(session_id: str, user: User = Depends(get_current_user)):
    """
    Get file assignments for resuming an interrupted upload.

    CLI calls this after ctrl-c to know which files go to which workers.
    """
    from sxd_core.clickhouse import ClickHouseManager

    ch = ClickHouseManager()
    session = ch.get_upload_session(session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "session_id": session_id,
        "status": session["status"],
        "assignments": session.get("node_assignments", {}),
        "files_received": session["files_received"],
        "total_files": session["total_files"],
        "bytes_received": session["bytes_received"],
        "total_bytes": session["total_bytes"],
    }


# --- Pipeline Endpoints ---


@app.post("/api/pipelines/publish")
async def publish_pipeline(
    file: UploadFile = File(...), user: User = Depends(get_current_user)
):
    """Receive a pipeline bundle, extract it, and start a build."""
    content = await file.read()
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing filename")
    pipeline_name = file.filename.split(".")[0]

    auth = get_auth_manager()
    if not auth.check_permission(user, "pipeline", "write"):
        raise HTTPException(status_code=403, detail="Permission denied: pipeline:write")

    build_dir = Path(f".temp/builds/{pipeline_name}")

    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir(parents=True, exist_ok=True)

    try:
        with tarfile.open(fileobj=io.BytesIO(content)) as tar:
            tar.extractall(path=build_dir)

        # Try to find Dockerfile in build_dir
        dockerfile = build_dir / "Dockerfile"
        if not dockerfile.exists():
            potential = list(build_dir.glob("Dockerfile*"))
            if potential:
                dockerfile = potential[0]
            else:
                raise HTTPException(
                    status_code=400, detail="No Dockerfile found in bundle"
                )

        image_tag = await build_engine.build_pipeline(
            name=pipeline_name,
            dockerfile_path=dockerfile,
            context_path=build_dir,
            tag="latest",
        )
        return {"status": "success", "pipeline": pipeline_name, "image": image_tag}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# --- Health & Metrics ---


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/nodes")
async def list_nodes(user: User = Depends(get_current_user)):
    """List available worker nodes and their current status."""
    from sxd_core.ops.node_metrics import get_all_node_metrics

    try:
        metrics = get_all_node_metrics()
        return {
            "nodes": [
                {
                    "node": node,
                    "disk_available_gb": m.disk_available_bytes / 1e9,
                    "cpu_cores": m.cpu_cores,
                    "pending_queue_mb": m.pending_queue_bytes / 1e6,
                    "score": 0.0,
                }
                for node, m in metrics.items()
            ],
            "count": len(metrics),
        }
    except Exception as e:
        return {"error": str(e), "nodes": [], "count": 0}


# --- Startup ---


@app.on_event("startup")
async def startup_event():
    # Add some default rules for demo
    trigger_service.add_rule(TriggerRule(name="Default Video", pipeline="video"))

    # Start the trigger service in the background
    asyncio.create_task(trigger_service.start())


def main():
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
