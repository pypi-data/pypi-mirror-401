import pytest
from temporalio.worker import Worker
from temporalio.testing import WorkflowEnvironment
from sxd_core.testing.temporal_test_workflows import HelloWorkflow, hello_activity


@pytest.mark.asyncio
async def test_real_temporal_sqlite():
    """
    Verify that we can run a real Temporal workflow using the SQLite-backed server.
    """
    # Start local Temporal server (uses SQLite by default)
    async with await WorkflowEnvironment.start_local() as env:
        task_queue = "hello-task-queue"

        # Start a worker
        async with Worker(
            env.client,
            task_queue=task_queue,
            workflows=[HelloWorkflow],
            activities=[hello_activity],
        ):
            # Execute workflow
            result = await env.client.execute_workflow(
                HelloWorkflow.run,
                "World",
                id="hello-workflow",
                task_queue=task_queue,
            )

            assert result == "Hello, World!"
