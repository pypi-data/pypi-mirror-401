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

from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog

from mistralai_workflows.worker.activity import context_var_task_queue
from mistralai_workflows.worker.sticky_worker_session.get_sticky_worker_session import get_sticky_worker_session
from mistralai_workflows.worker.sticky_worker_session.sticky_worker_session import StickyWorkerSession
from mistralai_workflows.worker.utils import reset_contextvar

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def run_sticky_worker_session(
    sticky_worker_session: StickyWorkerSession | None = None,
) -> AsyncGenerator[None, None]:
    """
    Run activities on the same worker.

    Args:
        sticky_worker_session: The sticky worker session to use.
    """
    if sticky_worker_session is None:
        sticky_worker_session = await get_sticky_worker_session()
    token = context_var_task_queue.set(sticky_worker_session.task_queue)
    try:
        yield
    finally:
        reset_contextvar(context_var_task_queue, token)
