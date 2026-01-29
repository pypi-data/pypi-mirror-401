import asyncio
import re
from pathlib import Path
import os

try:
    from docker import from_env as docker_from_env  # type: ignore
except ImportError:
    docker_from_env = None  # type: ignore

from sxd_core.logging import get_logger

log = get_logger("sxd.master.build")

# Docker registries
LOCAL_REGISTRY = "localhost:5000"
PUBLIC_REGISTRY = "ghcr.io/sentient-x"


def get_default_registry() -> str:
    """Get the default registry based on environment.

    Returns:
        The registry URL to use for images.
    """
    return os.getenv("SXD_REGISTRY", LOCAL_REGISTRY)


SXD_BASE_IMAGES = [
    f"{PUBLIC_REGISTRY}/sxd-base",
    f"{PUBLIC_REGISTRY}/sxd-pytorch",
    f"{PUBLIC_REGISTRY}/sxd-opencv",
    f"{PUBLIC_REGISTRY}/sxd-cuda",
]


class InvalidDockerfileError(Exception):
    """Raised when a Dockerfile doesn't derive from an SXD base image."""

    pass


class BuildEngine:
    def __init__(self, registry_url: str | None = None):
        self.registry_url = registry_url or get_default_registry()
        if docker_from_env:
            self.docker_client = docker_from_env()
        else:
            self.docker_client = None

    def _validate_dockerfile(self, dockerfile_path: Path) -> str:
        """
        Validate that a Dockerfile derives from an SXD base image.

        Args:
            dockerfile_path: Path to the Dockerfile.

        Returns:
            The base image name found in the FROM instruction.

        Raises:
            InvalidDockerfileError: If the Dockerfile doesn't use an SXD base image.
        """
        if not dockerfile_path.exists():
            raise FileNotFoundError(f"Dockerfile not found: {dockerfile_path}")

        content = dockerfile_path.read_text()
        # Look for FROM instruction, ignoring comments and Case Insensitive
        match = re.search(r"^\s*FROM\s+([^\s]+)", content, re.MULTILINE | re.IGNORECASE)

        if not match:
            raise InvalidDockerfileError("No FROM instruction found in Dockerfile")

        base_image = match.group(1)

        # Check if derived from SXD base image
        is_sxd_base = any(base_image.startswith(sxd_img) for sxd_img in SXD_BASE_IMAGES)

        if not is_sxd_base:
            raise InvalidDockerfileError(
                f"Dockerfile must derive from an SXD base image (e.g., sxd-base:latest), but found: {base_image}"
            )

        return base_image

    async def build_pipeline(
        self,
        name: str,
        dockerfile_path: Path,
        context_path: Path,
        tag: str = "latest",
        build_args: dict[str, str] | None = None,
    ) -> str:
        """
        Build a pipeline Docker image.

        Args:
            name: Name of the pipeline.
            dockerfile_path: Path to the Dockerfile.
            context_path: Path to the build context.
            tag: Tag for the image.
            build_args: Build arguments.

        Returns:
            The full image name and tag.
        """
        # Validate Dockerfile
        self._validate_dockerfile(dockerfile_path)

        image_name = f"{self.registry_url}/{name}"
        full_tag = f"{image_name}:{tag}"

        log.info("building pipeline image", name=name, tag=tag)

        # Build image using docker SDK (run in thread pool as it's blocking)
        loop = asyncio.get_event_loop()

        def _build():
            if not self.docker_client:
                raise RuntimeError("Docker is not available")
            return self.docker_client.images.build(
                path=str(context_path),
                dockerfile=str(dockerfile_path),
                tag=full_tag,
                buildargs=build_args,
                rm=True,
            )

        try:
            image, logs = await loop.run_in_executor(None, _build)
            for line in logs:
                if "stream" in line:
                    log.debug(line["stream"].strip())

            log.info("pipeline image built successfully", image=full_tag)
            return full_tag

        except Exception as e:
            log.error("failed to build pipeline image", name=name, error=str(e))
            raise

    async def push_pipeline(self, image_tag: str) -> bool:
        """
        Push a pipeline image to the registry.

        Args:
            image_tag: The full image name and tag to push.

        Returns:
            True if push was successful.
        """
        log.info("pushing pipeline image", image=image_tag)

        loop = asyncio.get_event_loop()

        def _push():
            if not self.docker_client:
                raise RuntimeError("Docker is not available")
            return self.docker_client.images.push(image_tag, stream=True, decode=True)

        try:
            response = await loop.run_in_executor(None, _push)
            for line in response:
                if "status" in line:
                    log.debug(line["status"])
                if "error" in line:
                    log.error("push error", error=line["error"])
                    return False

            log.info("pipeline image pushed successfully", image=image_tag)
            return True

        except Exception as e:
            log.error("failed to push pipeline image", image=image_tag, error=str(e))
            return False


async def publish_pipeline(
    name: str,
    path: Path,
    registry: str | None = None,
    tag: str = "latest",
) -> str:
    """
    High-level API to build and push a pipeline.

    Args:
        name: Name of the pipeline.
        path: Root path of the pipeline (containing Dockerfile).
        registry: Custom registry URL.
        tag: Image tag.

    Returns:
        The published image name.
    """
    engine = BuildEngine(registry)

    dockerfile = path / "Dockerfile"
    if not dockerfile.exists():
        # Try finding any Dockerfile
        potential = list(path.glob("Dockerfile*"))
        if potential:
            dockerfile = potential[0]
        else:
            raise FileNotFoundError(f"No Dockerfile found in {path}")

    image_tag = await engine.build_pipeline(name, dockerfile, path, tag)

    # If registry is local, we might skip push or assume it's shared
    success = await engine.push_pipeline(image_tag)

    if not success:
        log.warning("push failed, but image is available locally", image=image_tag)

    return image_tag
