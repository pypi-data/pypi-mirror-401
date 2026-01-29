"""
Testing utilities for SXD pipelines.

Provides mock environments and simulators for testing workflows
and activities without requiring a running Temporal server.
"""

import asyncio
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Type, Union
from unittest.mock import MagicMock


@dataclass
class ActivityInfo:
    """Mock activity info for testing."""

    activity_id: str = "test-activity-1"
    activity_type: str = "test_activity"
    task_queue: str = "test-queue"
    attempt: int = 1
    workflow_id: str = "test-workflow-1"
    workflow_run_id: str = "test-run-1"


class MockActivityEnvironment:
    """Mock environment for testing activities.

    Use this to test activity functions without running Temporal.

    Example:
        async def test_my_activity():
            env = MockActivityEnvironment()

            # Run the activity
            result = await env.run(my_activity, "input_arg")

            assert result.success
            assert env.heartbeats == 1
    """

    def __init__(self):
        self.heartbeats: int = 0
        self.heartbeat_details: List[Any] = []
        self.info = ActivityInfo()
        self._cancelled = False

    def heartbeat(self, *details):
        """Record a heartbeat."""
        self.heartbeats += 1
        if details:
            self.heartbeat_details.extend(details)

    def cancel(self):
        """Simulate cancellation."""
        self._cancelled = True

    @property
    def is_cancelled(self) -> bool:
        return self._cancelled

    async def run(
        self,
        activity_fn: Callable,
        *args,
        **kwargs,
    ) -> Any:
        """Run an activity function in the mock environment.

        This patches the temporalio.activity module to use our mock.

        Args:
            activity_fn: The activity function to run
            *args: Arguments to pass to the activity
            **kwargs: Keyword arguments to pass

        Returns:
            Activity result
        """
        import sys
        from unittest.mock import patch

        # Create mock activity module
        mock_activity = MagicMock()
        mock_activity.heartbeat = self.heartbeat
        mock_activity.info.return_value = self.info

        # Mock logger
        mock_logger = MagicMock()
        mock_activity.logger = mock_logger

        # Patch and run
        with patch.dict(sys.modules, {"temporalio.activity": mock_activity}):
            if asyncio.iscoroutinefunction(activity_fn):
                return await activity_fn(*args, **kwargs)
            else:
                return activity_fn(*args, **kwargs)


@dataclass
class WorkflowExecution:
    """Record of a simulated workflow execution."""

    workflow_id: str
    activities_called: List[Dict[str, Any]] = field(default_factory=list)
    signals_received: List[Dict[str, Any]] = field(default_factory=list)
    queries_handled: List[Dict[str, Any]] = field(default_factory=list)
    child_workflows: List[str] = field(default_factory=list)
    result: Any = None
    error: Optional[str] = None


class WorkflowSimulator:
    """Simulator for testing workflows without Temporal.

    Allows you to test workflow logic by mocking activity executions.

    Example:
        async def test_my_workflow():
            sim = WorkflowSimulator()

            # Mock activity results
            sim.mock_activity("validate_input", ProcessingResult.ok())
            sim.mock_activity("process_data", ProcessingResult.ok("/output/path"))

            # Run workflow
            result = await sim.run(MyWorkflow, MyInput(source_url="test.mp4"))

            assert result.status == "success"
            assert sim.execution.activities_called == ["validate_input", "process_data"]
    """

    def __init__(self):
        self._activity_mocks: Dict[str, Any] = {}
        self._activity_errors: Dict[str, Exception] = {}
        self.execution: Optional[WorkflowExecution] = None

    def mock_activity(
        self,
        activity_name: str,
        result: Any = None,
        error: Optional[Exception] = None,
        side_effect: Optional[Callable] = None,
    ):
        """Mock an activity's result.

        Args:
            activity_name: Name of the activity to mock
            result: Result to return
            error: Exception to raise (instead of result)
            side_effect: Callable to invoke for dynamic results
        """
        if error:
            self._activity_errors[activity_name] = error
        elif side_effect:
            self._activity_mocks[activity_name] = side_effect
        else:
            self._activity_mocks[activity_name] = result

    def clear_mocks(self):
        """Clear all activity mocks."""
        self._activity_mocks.clear()
        self._activity_errors.clear()

    async def execute_activity(
        self,
        activity: Union[str, Callable],
        *args,
        **kwargs,
    ) -> Any:
        """Simulate activity execution.

        This is called by the workflow during simulation.
        """
        if callable(activity):
            activity_name = getattr(activity, "__name__", str(activity))
        else:
            activity_name = activity

        # Record the call
        if self.execution:
            self.execution.activities_called.append(
                {
                    "name": activity_name,
                    "args": args,
                    "kwargs": kwargs,
                }
            )

        # Check for error mock
        if activity_name in self._activity_errors:
            raise self._activity_errors[activity_name]

        # Check for result mock
        if activity_name in self._activity_mocks:
            mock = self._activity_mocks[activity_name]
            if callable(mock):
                return mock(*args, **kwargs)
            return mock

        # No mock - return None with warning
        import warnings

        warnings.warn(f"Activity '{activity_name}' not mocked, returning None")
        return None

    async def run(
        self,
        workflow_class: Type,
        input_data: Any,
        workflow_id: str = "test-workflow-1",
    ) -> Any:
        """Run a workflow in simulation mode.

        Args:
            workflow_class: The workflow class to run
            input_data: Input to pass to the workflow
            workflow_id: Simulated workflow ID

        Returns:
            Workflow result
        """
        self.execution = WorkflowExecution(workflow_id=workflow_id)

        # Create workflow instance
        instance = workflow_class()

        # Inject our mock execute_activity
        original_execute_activity = getattr(instance, "execute_activity", None)
        instance.execute_activity = self.execute_activity

        try:
            # Find and run the workflow's run method
            run_method = getattr(instance, "run", None)
            if run_method is None:
                raise ValueError(f"Workflow {workflow_class} has no 'run' method")

            if asyncio.iscoroutinefunction(run_method):
                result = await run_method(input_data)
            else:
                result = run_method(input_data)

            self.execution.result = result
            return result

        except Exception as e:
            self.execution.error = str(e)
            raise
        finally:
            if original_execute_activity:
                instance.execute_activity = original_execute_activity


# Pytest fixtures (importable in conftest.py)


def activity_environment():
    """Pytest fixture for activity testing.

    Usage in conftest.py:
        from sxd_sdk.testing import activity_environment

    Usage in tests:
        async def test_my_activity(activity_environment):
            result = await activity_environment.run(my_activity, "arg")
    """
    return MockActivityEnvironment()


def workflow_simulator():
    """Pytest fixture for workflow testing.

    Usage in conftest.py:
        from sxd_sdk.testing import workflow_simulator

    Usage in tests:
        async def test_my_workflow(workflow_simulator):
            workflow_simulator.mock_activity("step1", result)
            result = await workflow_simulator.run(MyWorkflow, input_data)
    """
    return WorkflowSimulator()
