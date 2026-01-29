import asyncio
from typing import List, Optional
from pydantic import BaseModel
from sxd_core.clickhouse import ClickHouseManager
from temporalio.client import Client
from sxd_core.logging import get_logger

log = get_logger("sxd.master.trigger")


class TriggerRule(BaseModel):
    name: str
    pipeline: str
    customer_id: Optional[str] = None
    metadata_match: dict = {}


class TriggerService:
    def __init__(self, temporal_host: str = "localhost", temporal_port: int = 7233):
        self.ch = ClickHouseManager()
        self.temporal_host = temporal_host
        self.temporal_port = temporal_port
        self.rules: List[TriggerRule] = []
        self._running = False

    def add_rule(self, rule: TriggerRule):
        self.rules.append(rule)
        log.info(f"Added trigger rule: {rule.name} -> {rule.pipeline}")

    async def start(self):
        self._running = True
        log.info("Trigger service started")

        # Connect to Temporal
        client = await Client.connect(f"{self.temporal_host}:{self.temporal_port}")

        while self._running:
            try:
                await self._check_for_new_data(client)
            except Exception as e:
                log.error(f"Error checking for new data: {e}")
            await asyncio.sleep(10)  # Poll interval

    async def trigger_workflow(self, workflow_name: str, input_data: dict):
        """
        Request-Response trigger.
        Calls the workflow directly.
        """
        log.info(f"Manual trigger requested: {workflow_name}")
        client = await Client.connect(f"{self.temporal_host}:{self.temporal_port}")
        await self._execute_pipeline(client, workflow_name, input_data)

    async def _check_for_new_data(self, client: Client):
        # Query episodes that haven't been processed yet
        query = f"SELECT id, customer_id, source_path FROM {self.ch.database}.episodes WHERE processing_status = 'PENDING' LIMIT 10"
        episodes = self.ch.execute_query(query)

        for ep in episodes:
            log.info(f"Found pending episode: {ep['id']}")

            # Match against rules
            matches = []
            for rule in self.rules:
                if rule.customer_id and rule.customer_id != ep["customer_id"]:
                    continue

                # Metadata matching logic (simplified)
                matches.append(rule)

            if matches:
                # Mark as PROCESSING first to prevent re-triggering on next poll
                self._mark_episode_processing(ep["id"])
                
                log.info(
                    f"Found {len(matches)} matching pipelines for episode {ep['id']}"
                )
                for rule in matches:
                    await self._execute_pipeline(client, rule.pipeline, ep)

    def _mark_episode_processing(self, episode_id: str):
        """Atomically mark episode as PROCESSING to prevent duplicate triggers."""
        # Use ALTER UPDATE with version check for atomicity
        # ClickHouse's ALTER UPDATE is atomic per-partition
        query = f"""
            ALTER TABLE {self.ch.database}.episodes
            UPDATE processing_status = 'PROCESSING'
            WHERE id = '{episode_id}' AND processing_status = 'PENDING'
        """
        try:
            self.ch.execute_query(query)
            log.debug(f"Marked episode {episode_id} as PROCESSING")
        except Exception as e:
            log.warning(f"Failed to mark episode {episode_id} as PROCESSING: {e}")

    async def _execute_pipeline(
        self, client: Client, workflow_name: str, episode: dict
    ):
        from sxd_core.registry import get_workflow, get_app_config

        # 1. Resolve workflow and app context
        wf_defn = get_workflow(workflow_name)
        if not wf_defn:
            log.error(f"Workflow {workflow_name} not found in registry")
            return

        app_cfg = None
        if wf_defn.app_name:
            app_cfg = get_app_config(wf_defn.app_name)

        # 2. Determine task queue
        task_queue = wf_defn.task_queue
        if app_cfg:
            # Overwrite if app has specific queue configuration
            for wf_cfg in app_cfg.workflows:
                if wf_cfg.name == workflow_name:
                    task_queue = wf_cfg.task_queue
                    break

        log.info(
            f"Starting workflow {workflow_name} for app {wf_defn.app_name or 'none'} on queue {task_queue}"
        )

        try:
            # Note: temporalio Client.start_workflow takes the nickname or the class
            await client.start_workflow(
                workflow_name,
                arg=episode,
                id=f"trigger-{workflow_name}-{episode.get('id', 'req-resp')}",
                task_queue=task_queue,
            )
            log.info(f"✓ Workflow {workflow_name} started")
        except Exception as e:
            log.error(f"✗ Failed to start workflow {workflow_name}: {e}")
