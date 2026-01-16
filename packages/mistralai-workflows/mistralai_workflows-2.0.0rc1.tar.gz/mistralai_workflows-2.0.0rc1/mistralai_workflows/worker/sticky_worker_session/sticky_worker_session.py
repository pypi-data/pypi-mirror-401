"""
Activity decorator and related functionality for defining Temporal activities.

This module provides the `@activity` decorator for defining Temporal activities with various
configuration options. Activities are the basic units of work in Temporal workflows.

Key Features:
- Decorator for defining activities with timeout and retry policies
- Support for activity inheritance via `extends` parameter
- Worker-scoped activities for task queue isolation
- Dependency injection integration
- Automatic registration with Temporal worker
- Context management for scoped worker task queues
"""

from typing import Callable

import structlog
from pydantic import BaseModel

logger = structlog.get_logger(__name__)

_ACTIVITY_STICKY_TO_WORKER_ATTR_NAME = "__abraxas_activity_sticky_to_worker"


class StickyWorkerSession(BaseModel):
    """Model representing a worker's task queue scope.

    This model is used to track which task queue a worker is currently scoped to.
    When activities are marked as `scoped_to_worker=True`, they will only execute
    on the task queue specified in this model.

    Attributes:
        task_queue: The name of the task queue that the worker is scoped to
    """

    task_queue: str


def set_activity_as_sticky_to_worker(activity: Callable) -> None:
    """
    Mark an activity as sticky to a specific worker.

    This internal function sets a special attribute on the activity function
    to indicate it should be executed on the same worker when called within
    a sticky worker session.

    Args:
        activity: The activity function to mark as sticky.
    """
    setattr(activity, _ACTIVITY_STICKY_TO_WORKER_ATTR_NAME, True)


def check_activity_is_sticky_to_worker(activity: Callable) -> bool:
    """
    Check if an activity is marked as sticky to a worker.

    Args:
        activity: The activity function to check.

    Returns:
        bool: True if the activity is sticky to a worker, False otherwise.
    """
    return getattr(activity, _ACTIVITY_STICKY_TO_WORKER_ATTR_NAME, False)
