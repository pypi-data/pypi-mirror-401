import asyncio
from typing import Any, Type

import structlog
import temporalio.activity
import temporalio.client
import temporalio.worker
import temporalio.workflow

from mistralai_workflows.protocol.v1.events import (
    ActivityTaskCompleted,
    ActivityTaskCompletedAttributes,
    ActivityTaskFailed,
    ActivityTaskFailedAttributes,
    ActivityTaskRetrying,
    ActivityTaskRetryingAttributes,
    ActivityTaskStarted,
    ActivityTaskStartedAttributes,
    Failure,
    JSONPayload,
    WorkflowEvent,
    WorkflowExecutionCanceled,
    WorkflowExecutionCanceledAttributes,
    WorkflowExecutionCompleted,
    WorkflowExecutionCompletedAttributes,
    WorkflowExecutionFailed,
    WorkflowExecutionFailedAttributes,
    WorkflowExecutionStarted,
    WorkflowExecutionStartedAttributes,
)
from mistralai_workflows.worker.events.event_context import EventContext
from mistralai_workflows.worker.events.event_utils import create_base_event_fields, should_publish_event

logger = structlog.get_logger(__name__)


def _publish_event(event: WorkflowEvent, *, check_replay: bool = False) -> None:
    """Publish event via the EventContext.

    Args:
        event: The event to publish.
        check_replay: If True, skip publishing during workflow replay.
    """
    if check_replay and not should_publish_event():
        return

    context = EventContext.get_singleton()
    if not context:
        logger.warning(
            "EventContext not available, skipping event",
            event_type=event.event_type,
        )
        return
    context.publish_event(event)


class _EventActivityInboundInterceptor(temporalio.worker.ActivityInboundInterceptor):
    """Activity interceptor that sends activity task events to the API.

    Emits ACTIVITY_TASK_STARTED, ACTIVITY_TASK_COMPLETED, ACTIVITY_TASK_RETRYING,
    and ACTIVITY_TASK_FAILED events.
    """

    async def execute_activity(self, input: temporalio.worker.ExecuteActivityInput) -> Any:
        context = EventContext.get_singleton()
        if not context:
            return await self.next.execute_activity(input)

        activity_info = temporalio.activity.info()
        task_id = activity_info.activity_id
        activity_name = activity_info.activity_type
        attempt = activity_info.attempt

        max_attempts = 1
        if activity_info.retry_policy and activity_info.retry_policy.maximum_attempts > 0:
            max_attempts = activity_info.retry_policy.maximum_attempts

        if attempt == 1:
            _publish_event(
                ActivityTaskStarted(
                    **create_base_event_fields(),
                    attributes=ActivityTaskStartedAttributes(
                        task_id=task_id,
                        activity_name=activity_name,
                        input=JSONPayload(value=list(input.args)),
                    ),
                )
            )

        try:
            result = await self.next.execute_activity(input)
            _publish_event(
                ActivityTaskCompleted(
                    **create_base_event_fields(),
                    attributes=ActivityTaskCompletedAttributes(
                        task_id=task_id,
                        activity_name=activity_name,
                        result=JSONPayload(value=result),
                    ),
                )
            )
            return result

        except Exception as e:
            is_final_attempt = max_attempts > 0 and attempt >= max_attempts

            if is_final_attempt:
                _publish_event(
                    ActivityTaskFailed(
                        **create_base_event_fields(),
                        attributes=ActivityTaskFailedAttributes(
                            task_id=task_id,
                            activity_name=activity_name,
                            attempt=attempt,
                            failure=Failure(message=str(e)),
                        ),
                    )
                )
            else:
                _publish_event(
                    ActivityTaskRetrying(
                        **create_base_event_fields(),
                        attributes=ActivityTaskRetryingAttributes(
                            task_id=task_id,
                            activity_name=activity_name,
                            attempt=attempt,
                            failure=Failure(message=str(e)),
                        ),
                    )
                )
            raise


class _EventWorkflowInboundInterceptor(temporalio.worker.WorkflowInboundInterceptor):
    """Workflow interceptor that sends workflow execution events to the API.

    Emits WORKFLOW_EXECUTION_STARTED, WORKFLOW_EXECUTION_COMPLETED,
    WORKFLOW_EXECUTION_FAILED, and WORKFLOW_EXECUTION_CANCELED events.
    """

    async def execute_workflow(self, input: temporalio.worker.ExecuteWorkflowInput) -> Any:
        context = EventContext.get_singleton()
        if not context:
            return await super().execute_workflow(input)

        info = temporalio.workflow.info()
        task_id = str(temporalio.workflow.uuid4())

        _publish_event(
            WorkflowExecutionStarted(
                **create_base_event_fields(),
                attributes=WorkflowExecutionStartedAttributes(
                    task_id=task_id,
                    workflow_name=info.workflow_type,
                    input=JSONPayload(value=list(input.args)),
                ),
            ),
            check_replay=True,
        )

        try:
            result = await super().execute_workflow(input)
            _publish_event(
                WorkflowExecutionCompleted(
                    **create_base_event_fields(),
                    attributes=WorkflowExecutionCompletedAttributes(
                        task_id=task_id,
                        result=JSONPayload(value=result),
                    ),
                ),
                check_replay=True,
            )
            return result

        except asyncio.CancelledError as e:
            _publish_event(
                WorkflowExecutionCanceled(
                    **create_base_event_fields(),
                    attributes=WorkflowExecutionCanceledAttributes(
                        task_id=task_id,
                        reason=str(e) if str(e) else None,
                    ),
                ),
                check_replay=True,
            )
            raise

        except Exception as e:
            _publish_event(
                WorkflowExecutionFailed(
                    **create_base_event_fields(),
                    attributes=WorkflowExecutionFailedAttributes(
                        task_id=task_id,
                        failure=Failure(message=str(e)),
                    ),
                ),
                check_replay=True,
            )
            raise


class EventInterceptor(temporalio.client.Interceptor, temporalio.worker.Interceptor):
    """Temporal interceptor that sends workflow and activity events to the Workflows API.

    Captures workflow lifecycle events (started, completed, failed, canceled)
    and activity lifecycle events (started, completed, retrying, failed).
    Events are published asynchronously via the EventContext's task group.
    """

    def intercept_activity(
        self, next: temporalio.worker.ActivityInboundInterceptor
    ) -> temporalio.worker.ActivityInboundInterceptor:
        return _EventActivityInboundInterceptor(next)

    def workflow_interceptor_class(
        self, input: temporalio.worker.WorkflowInterceptorClassInput
    ) -> Type[temporalio.worker.WorkflowInboundInterceptor] | None:
        return _EventWorkflowInboundInterceptor
