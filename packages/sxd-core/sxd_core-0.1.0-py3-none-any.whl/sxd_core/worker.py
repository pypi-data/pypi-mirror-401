"""Unified Worker for SXD Platform."""

import asyncio
import concurrent.futures
import os
from typing import Callable, Optional

from temporalio.client import Client
from temporalio.worker import Worker

from sxd_core.logging import get_logger
from sxd_core.registry import list_activities, list_workflows

log = get_logger("sxd.worker")


async def start_worker(
    worker_count: int,
    temporal_host: str,
    temporal_port: int,
    pipeline_loader: Optional[Callable] = None,
    namespace: str = "default",
    queues: Optional[list[str]] = None,
    app_name: Optional[str] = None,
):
    """
    Start the unified Temporal worker with optional dynamic reloading and app isolation.
    """
    # 1. Initial load
    if pipeline_loader:
        log.info("initial pipeline load...")
        pipeline_loader()

    # 2. Get registered components
    workflows_map = list_workflows()
    activities_map = list_activities()

    if app_name:
        log.info("Starting worker for specific app", app_name=app_name)
        workflows_map = {
            k: v for k, v in workflows_map.items() if v.app_name == app_name
        }
        if not workflows_map:
            log.warning(
                "No workflows found for app, starting empty worker", app_name=app_name
            )

    # 3. Connect to Temporal
    log.info(
        "connecting to temporal",
        host=temporal_host,
        port=temporal_port,
        namespace=namespace,
    )
    try:
        client = await Client.connect(
            f"{temporal_host}:{temporal_port}", namespace=namespace
        )
    except Exception as e:
        log.error("failed to connect to temporal", error=str(e))
        raise

    # 4. Group by Task Queue
    # We want to start a Worker for every unique task queue found in workflows.
    # Activities are shared across all queues (or at least offered to all).

    queues_set = set()
    if queues:
        queues_set.update(queues)
    else:
        for wf in workflows_map.values():
            queues_set.add(wf.task_queue)

    # Add node-specific queue for targeted activities (e.g. checksum verification)
    node_id = os.getenv("SXD_NODE_ID") or os.getenv("SXD_NODE_IP")
    if node_id:
        queues_set.add(f"node-{node_id}")
        log.info("adding node-specific task queue", queue=f"node-{node_id}")

    if not queues_set:
        queues_set.add("default")

    log.info("found task queues", queues=list(queues_set))

    workers = []

    # 5. Create Workers
    # ...
    shared_executor = concurrent.futures.ThreadPoolExecutor(max_workers=worker_count)

    all_workflows = [wf.workflow_class for wf in workflows_map.values()]
    all_activities = [act.func for act in activities_map.values()]

    # Filter empty/none
    all_workflows = [w for w in all_workflows if w is not None]
    all_activities = [a for a in all_activities if a is not None]

    log.info(
        "registering components",
        workflow_count=len(all_workflows),
        activity_count=len(all_activities),
    )

    for q in queues_set:
        # Queue Design: We register ALL workflows/activities with EACH worker.
        # Temporal Server routes tasks to workers based on queue subscription.
        # Unused workflow definitions on a queue are harmless (never instantiated).
        # Our registry binds workflows to queues, but workers accept all for simplicity.

        w = Worker(
            client,
            task_queue=q,
            workflows=all_workflows,
            activities=all_activities,
            activity_executor=shared_executor,
            max_concurrent_activities=worker_count,
            # max_concurrent_workflow_tasks? Default is fine.
        )
        workers.append(w)
        log.info("initialized worker", task_queue=q)

    # 6. Run all workers
    log.info("starting workers", count=len(workers))
    try:
        await asyncio.gather(*[w.run() for w in workers])
    except (KeyboardInterrupt, asyncio.CancelledError):
        log.info("shutting down workers")
    finally:
        shared_executor.shutdown(wait=False)
