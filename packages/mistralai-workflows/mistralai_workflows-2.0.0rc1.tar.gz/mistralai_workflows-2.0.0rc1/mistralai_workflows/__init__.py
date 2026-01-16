from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("mistralai-workflows")
except PackageNotFoundError:
    __version__ = "0.0.0.dev0"


from .client import WorkflowsClient
from .common.models import (
    ScheduleCalendar,
    ScheduleInterval,
    ScheduleOverlapPolicy,
    SchedulePolicy,
    ScheduleRange,
)
from .common.models import ScheduleDefinition as Schedule
from .worker import agents
from .worker.activity import activity
from .worker.concurrency import (
    ExtraItemParams,
    GetItemFromIndexParams,
    execute_activities_in_parallel,
)
from .worker.config import AppConfig as WorkflowsConfig
from .worker.config import config
from .worker.dependency_injector import DependencyInjector, Depends
from .worker.exceptions import ActivityError, WorkflowError
from .worker.interactive_workflow import InteractiveWorkflow
from .worker.local_activity import run_activities_locally
from .worker.rate_limit import RateLimit
from .worker.sdk_workflows_migration import (  # Temporal migration helpers
    workflows,
    workflows_mistralai,
)
from .worker.sticky_worker_session.get_sticky_worker_session import (
    get_sticky_worker_session,
)
from .worker.sticky_worker_session.run_sticky_worker_session import (
    run_sticky_worker_session,
)
from .worker.sticky_worker_session.sticky_worker_session import StickyWorkerSession
from .worker.task import task, task_from
from .worker.worker import run_worker
from .worker.workflow import workflow
from .worker.workflow_definition import get_workflow_definition
from .worker.workflow_execution import execute_workflow, get_execution_id

__all__ = [
    "activity",
    "run_worker",
    "workflow",
    # Workflow utilities
    "get_workflow_definition",
    "execute_workflow",
    "get_execution_id",
    "InteractiveWorkflow",
    # Core classes
    "WorkflowsConfig",
    "config",
    "Depends",
    "DependencyInjector",
    "WorkflowsClient",
    "WorkflowError",
    "ActivityError",
    "Schedule",
    "ScheduleCalendar",
    "ScheduleInterval",
    "ScheduleOverlapPolicy",
    "SchedulePolicy",
    "ScheduleRange",
    "ExtraItemParams",
    "execute_activities_in_parallel",
    "GetItemFromIndexParams",
    "run_sticky_worker_session",
    "get_sticky_worker_session",
    "StickyWorkerSession",
    "run_activities_locally",
    "RateLimit",
    "agents",
    "task",
    "task_from",
    "workflows",  # Temporal migration helpers
    "workflows_mistralai",  # Temporal migration helpers
]
