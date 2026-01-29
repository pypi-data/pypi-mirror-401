import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from sxd_master.trigger import TriggerService, TriggerRule


@pytest.fixture
def mock_ch():
    with patch("sxd_master.trigger.ClickHouseManager") as mock:
        instance = mock.return_value
        instance.database = "sxd"
        yield instance


@pytest.fixture
def mock_workflow_registry():
    """Mock the workflow registry to return workflow definitions."""
    from sxd_core.registry import WorkflowDefinition

    mock_workflows = {
        "video-pipeline": WorkflowDefinition(
            nickname="video-pipeline",
            workflow_class=MagicMock(),
            input_type=dict,
            task_queue="video-processing",
        ),
        "cust1-pipeline": WorkflowDefinition(
            nickname="cust1-pipeline",
            workflow_class=MagicMock(),
            input_type=dict,
            task_queue="video-processing",
        ),
        "test-pipeline": WorkflowDefinition(
            nickname="test-pipeline",
            workflow_class=MagicMock(),
            input_type=dict,
            task_queue="video-processing",
        ),
    }

    with patch(
        "sxd_core.registry.get_workflow",
        side_effect=lambda name: mock_workflows.get(name),
    ):
        yield mock_workflows


@pytest.fixture
def trigger_service(mock_ch):
    return TriggerService(temporal_host="localhost", temporal_port=7233)


@pytest.mark.asyncio
async def test_trigger_service_rule_matching(
    trigger_service, mock_ch, mock_workflow_registry
):
    # Setup rules
    trigger_service.add_rule(TriggerRule(name="all-videos", pipeline="video-pipeline"))
    trigger_service.add_rule(
        TriggerRule(name="cust1-only", pipeline="cust1-pipeline", customer_id="cust1")
    )

    # Mock pending data from ClickHouse
    mock_ch.execute_query.return_value = [
        {"id": "ep1", "customer_id": "cust1", "source_path": "/data/ep1"},
        {"id": "ep2", "customer_id": "cust2", "source_path": "/data/ep2"},
    ]

    mock_client = MagicMock()
    mock_client.start_workflow = AsyncMock()

    # Run matching check
    await trigger_service._check_for_new_data(mock_client)

    # Verify calls
    # ep1 should match both rules
    # ep2 should match only "all-videos"

    # Total calls: 2 (ep1) + 1 (ep2) = 3
    assert mock_client.start_workflow.call_count == 3

    # Verify specific triggers
    calls = mock_client.start_workflow.call_args_list
    triggered_pipelines = [c[0][0] for c in calls]
    assert triggered_pipelines.count("video-pipeline") == 2
    assert triggered_pipelines.count("cust1-pipeline") == 1


@pytest.mark.asyncio
async def test_trigger_service_execute_pipeline(
    trigger_service, mock_workflow_registry
):
    mock_client = MagicMock()
    mock_client.start_workflow = AsyncMock()

    episode = {"id": "ep123", "customer_id": "cust1"}
    await trigger_service._execute_pipeline(mock_client, "test-pipeline", episode)

    mock_client.start_workflow.assert_called_once_with(
        "test-pipeline",
        arg=episode,
        id="trigger-test-pipeline-ep123",
        task_queue="video-processing",
    )
