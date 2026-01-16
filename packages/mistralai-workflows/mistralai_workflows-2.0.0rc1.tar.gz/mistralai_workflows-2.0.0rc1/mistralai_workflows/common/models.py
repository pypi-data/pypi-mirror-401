import base64
import textwrap
import uuid
from datetime import datetime, timedelta
from enum import StrEnum
from typing import Any, Dict, List, Literal, Sequence

import temporalio
import temporalio.client
from pydantic import BaseModel, Field
from temporalio.client import ScheduleOverlapPolicy


class SearchAttributes(StrEnum):
    otel_trace_id = "OtelTraceId"
    workflow_name = "WorkflowName"
    allow_auto_remove = "AllowAutoRemove"


class EventAttributes(StrEnum):
    type = "abraxas.type"
    id = "abraxas.id"
    event_type = "abraxas.event_type"
    arguments = "abraxas.arguments"
    result = "abraxas.result"
    internal = "abraxas.internal"

    activity_execution_id = "abraxas.activity.execution_id"
    activity_attempt = "abraxas.activity.attempt"
    activity_max_attempts = "abraxas.activity.max_attempts"

    workflow_id = "abraxas.workflow.id"
    workflow_execution_id = "abraxas.workflow.execution_id"
    workflow_type = "abraxas.workflow.type"
    workflow_duration_ms = "abraxas.workflow.duration.ms"
    workflow_attempt = "abraxas.workflow.attempt"
    workflow_max_attempts = "abraxas.workflow.max_attempts"

    progress_status = "abraxas.progress.status"
    progress_start_time_unix_ms = "abraxas.progress.start_time_unix_ms"
    progress_end_time_unix_ms = "abraxas.progress.end_time_unix_ms"
    progress_error = "abraxas.progress.error"

    custom_prefix = "abraxas.custom"


class EventSpanType(StrEnum):
    workflow_init = "workflow_init"
    workflow_report = "workflow_report"
    activity = "activity"
    signal = "signal"
    update = "update"
    query = "query"
    event = "event"


class EncodedPayloadOptions(StrEnum):
    OFFLOADED = "offloaded"
    ENCRYPTED = "encrypted"
    PARTIALLY_ENCRYPTED = "encrypted-partial"


class WorkflowContext(BaseModel):
    namespace: str
    execution_id: str
    parent_workflow_exec_id: str | None = None
    root_workflow_exec_id: str | None = None


class EncodedPayload(BaseModel):
    context: WorkflowContext
    encoding_options: list[EncodedPayloadOptions] = Field(description="The encoding of the payload", default=[])
    payload: bytes = Field(description="The encoded payload")


class EncryptableFieldTypes(StrEnum):
    STRING = "__encrypted_str__"


class EncryptedStrField(BaseModel):
    field_type: Literal[EncryptableFieldTypes.STRING] = EncryptableFieldTypes.STRING
    data: str


class NetworkEncodedBase(BaseModel):
    b64payload: str = Field(description="The encoded payload")
    encoding_options: list[EncodedPayloadOptions] = Field(description="The encoding of the payload", default=[])


class PayloadMetadataKeys(StrEnum):
    ENCODING = "encoding"
    ENCODING_ORIGINAL = "encoding-orig"
    NAMESPACE = "namespace"
    EXECUTION_ID = "execution_id"
    PARENT_WORKFLOW_EXEC_ID = "parent_workflow_exec_id"
    ROOT_WORKFLOW_EXEC_ID = "root_workflow_exec_id"
    EMPTY_PAYLOAD = "empty_payload"
    ENCODING_OPTIONS = "encoding_options"

    IS_UNENCODED_MEMO = "is_unencoded_memo"


class NetworkEncodedInput(NetworkEncodedBase):
    empty: bool = Field(description="Whether the payload is empty", default=False)

    def to_encoded_payload(self, namespace: str, execution_id: str) -> EncodedPayload:
        return EncodedPayload(
            payload=base64.b64decode(self.b64payload),
            encoding_options=self.encoding_options,
            context=WorkflowContext(
                namespace=namespace,
                execution_id=execution_id,
            ),
        )

    @staticmethod
    def from_encoded_payload(encoded_payload: EncodedPayload) -> "NetworkEncodedInput":
        return NetworkEncodedInput(
            b64payload=base64.b64encode(encoded_payload.payload).decode("utf-8"),
            encoding_options=encoded_payload.encoding_options,
        )

    @staticmethod
    def from_data(data: bytes, encoding_options: list[EncodedPayloadOptions]) -> "NetworkEncodedInput":
        return NetworkEncodedInput(
            b64payload=base64.b64encode(data).decode("utf-8"),
            encoding_options=encoding_options,
        )


class NetworkEncodedResult(NetworkEncodedBase):
    @staticmethod
    def from_encoded_payload(encoded_payload: EncodedPayload) -> "NetworkEncodedResult":
        return NetworkEncodedResult(
            b64payload=base64.b64encode(encoded_payload.payload).decode("utf-8"),
            encoding_options=encoded_payload.encoding_options,
        )

    def get_payload(self) -> bytes:
        return base64.b64decode(self.b64payload)


class PayloadWithContext(BaseModel):
    """Format of payloads sent through temporal server"""

    context: WorkflowContext
    payload: Any
    empty: bool = False


class SignalDefinition(BaseModel):
    name: str = Field(description="Name of the signal")
    description: str | None = Field(default=None, description="Description of the signal")
    input_schema: Dict[str, Any] | None = Field(
        default=None,
        description="Input JSON schema of the signal's model",
        json_schema_extra={"additionalProperties": True},
    )
    # Signals don't have an output schema from the sender's perspective


class QueryDefinition(BaseModel):
    name: str = Field(description="Name of the query")
    description: str | None = Field(default=None, description="Description of the query")
    input_schema: Dict[str, Any] | None = Field(
        default=None,
        description="Input JSON schema of the query's model",
        json_schema_extra={"additionalProperties": True},
    )
    output_schema: Dict[str, Any] | None = Field(
        default=None,
        description="Output JSON schema of the query's model",
        json_schema_extra={"additionalProperties": True},
    )


class UpdateDefinition(BaseModel):
    name: str = Field(description="Name of the update")
    description: str | None = Field(default=None, description="Description of the update")
    input_schema: Dict[str, Any] | None = Field(
        default=None,
        description="Input JSON schema of the update's model",
        json_schema_extra={"additionalProperties": True},
    )
    output_schema: Dict[str, Any] | None = Field(
        default=None,
        description="Output JSON schema of the update's model",
        json_schema_extra={"additionalProperties": True},
    )


class ScheduleRange(BaseModel, temporalio.client.ScheduleRange, frozen=True):
    """Inclusive range for a schedule match value."""

    start: int
    """Inclusive start of the range."""

    end: int = 0
    """Inclusive end of the range.

    If unset or less than start, defaults to start.
    """

    step: int = 0
    """
    Step to take between each value.

    Unset or 0 defaults as 1.
    """


class ScheduleInterval(BaseModel, temporalio.client.ScheduleIntervalSpec):
    """Specification for scheduling on an interval.

    Matches times expressed as epoch + (n * every) + offset.
    """

    every: timedelta
    """Period to repeat the interval."""

    offset: timedelta | None = None
    """Fixed offset added to each interval period."""


class ScheduleCalendar(BaseModel, temporalio.client.ScheduleCalendarSpec):
    """Specification relative to calendar time when to run an action.

    A timestamp matches if at least one range of each field matches except for
    year. If year is missing, that means all years match. For all fields besides
    year, at least one range must be present to match anything.
    """

    second: Sequence[ScheduleRange] = (ScheduleRange(start=0),)
    """Second range to match, 0-59. Default matches 0."""

    minute: Sequence[ScheduleRange] = (ScheduleRange(start=0),)
    """Minute range to match, 0-59. Default matches 0."""

    hour: Sequence[ScheduleRange] = (ScheduleRange(start=0),)
    """Hour range to match, 0-23. Default matches 0."""

    day_of_month: Sequence[ScheduleRange] = (ScheduleRange(start=1, end=31),)
    """Day of month range to match, 1-31. Default matches all days."""

    month: Sequence[ScheduleRange] = (ScheduleRange(start=1, end=12),)
    """Month range to match, 1-12. Default matches all months."""

    year: Sequence[ScheduleRange] = ()
    """Optional year range to match. Default of empty matches all years."""

    day_of_week: Sequence[ScheduleRange] = (ScheduleRange(start=0, end=6),)
    """Day of week range to match, 0-6, 0 is Sunday. Default matches all
    days."""

    comment: str | None = None
    """Description of this schedule."""


# We need to redefine these as they are initially defined as dataclasses in Temporalio.
# Upon conversion to Pydantic models,
# all attributes become mandatory, which results in errors such as:
# ```
#   pydantic_core._pydantic_core.ValidationError: 3 validation errors for ScheduleDefinition
#   intervals
#     Field required [type=missing, input_value={'calendars': [Calendar(s...ep=1),), comment=None)]}, input_type=dict]
#       For further information visit https://errors.pydantic.dev/2.10/v/missing
#   ...
# ```
# When defining ScheduleDefinition as follows:
# ```
#   class ScheduleDefinition(BaseModel, temporalio.client.ScheduleSpec):
#       pass
# ```


class SchedulePolicy(BaseModel):
    catchup_window_seconds: int = Field(
        default=31536000,
        description=(
            "After a Temporal server is unavailable, amount of time in seconds in the past to execute missed actions."
        ),
    )
    overlap: ScheduleOverlapPolicy = Field(
        default=ScheduleOverlapPolicy.SKIP,
        description="Policy controlling what to do when a workflow is already running.",
    )
    pause_on_failure: bool = Field(default=False, description="Whether to pause the schedule after a workflow failure.")

    @property
    def catchup_window(self) -> timedelta:
        return timedelta(seconds=self.catchup_window_seconds)

    @catchup_window.setter
    def catchup_window(self, value: timedelta) -> None:
        self.catchup_window_seconds = int(value.total_seconds())


class ScheduleDefinition(BaseModel):
    """Specification of the times scheduled actions may occur.

    The times are the union of :py:attr:`calendars`, :py:attr:`intervals`, and
    :py:attr:`cron_expressions` excluding anything in :py:attr:`skip`.
    """

    input: Any = Field(description="Input to provide to the workflow when starting it.")

    calendars: List[ScheduleCalendar] = Field(
        default_factory=list, description="Calendar-based specification of times."
    )

    intervals: List[ScheduleInterval] = Field(
        default_factory=list, description="Interval-based specification of times."
    )

    cron_expressions: List[str] = Field(default_factory=list, description="Cron-based specification of times.")

    skip: List[ScheduleCalendar] = Field(default_factory=list, description="Set of calendar times to skip.")

    start_at: datetime | None = Field(default=None, description="Time after which the first action may be run.")

    end_at: datetime | None = Field(default=None, description="Time after which no more actions will be run.")

    jitter: timedelta | None = Field(
        default=None,
        description=textwrap.dedent("""
        Jitter to apply each action.

        An action's scheduled time will be incremented by a random value between 0
        and this value if present (but not past the next schedule).
        """),
    )

    time_zone_name: str | None = Field(default=None, description="IANA time zone name, for example ``US/Central``.")

    policy: SchedulePolicy = Field(default_factory=SchedulePolicy, description="Policy for the schedule.")


class WorkflowCodeDefinition(BaseModel):
    input_schema: Dict[str, Any] | None = Field(
        default=None,
        description="Input schema of the workflow's run method",
        json_schema_extra={"additionalProperties": True},
    )  # note change to Dict[str, Any] which is closer to real Json type.
    output_schema: Dict[str, Any] | None = Field(
        default=None,
        description="Output schema of the workflow's run method",
        json_schema_extra={"additionalProperties": True},
    )
    signals: List[SignalDefinition] = Field(default_factory=list, description="Signal handlers defined by the workflow")
    queries: List[QueryDefinition] = Field(default_factory=list, description="Query handlers defined by the workflow")
    updates: List[UpdateDefinition] = Field(default_factory=list, description="Update handlers defined by the workflow")


class WorkflowSpec(WorkflowCodeDefinition):
    name: str = Field(description="Name of the workflow")
    display_name: str | None = Field(default=None, description="Display name of the workflow")
    description: str | None = Field(default=None, description="Description of the workflow")
    schedules: List[ScheduleDefinition] = Field(default_factory=list, description="Schedules defined by the workflow")


class WorkflowSpecWithTaskQueue(WorkflowSpec):
    task_queue: str = Field(description="Task queue name for the workflow")


class WorkflowType(StrEnum):
    CODE = "code"
    # DSL = "dsl"


class Workflow(BaseModel):
    id: uuid.UUID = Field(description="Unique identifier of the workflow")
    name: str = Field(description="Name of the workflow")
    display_name: str = Field(description="Display name of the workflow")
    type: WorkflowType = Field(description="Type of the workflow")
    description: str | None = Field(default=None, description="Description of the workflow")
    customer_id: uuid.UUID = Field(description="Customer ID of the workflow")
    workspace_id: uuid.UUID = Field(description="Workspace ID of the workflow")


class WorkflowVersion(BaseModel):
    id: uuid.UUID = Field(description="Unique identifier of the workflow version")
    task_queue: str = Field(description="Project name of the workflow")
    definition: WorkflowCodeDefinition
    workflow_id: uuid.UUID = Field(description="Workflow ID of the workflow")
    workflow: Workflow | None = Field(default=None, description="Workflow of the workflow version")


class EventType(StrEnum):
    EVENT = "EVENT"
    """Standard event
    """

    EVENT_PROGRESS = "EVENT_PROGRESS"
    """Event progress event created using Task system context manager
    """


class EventProgressStatus(StrEnum):
    RUNNING = "RUNNING"
    """Event progress is running
    """

    COMPLETED = "COMPLETED"
    """Event progress has completed
    """

    FAILED = "FAILED"
    """Event progress has failed
    """


class BlobRef(BaseModel):
    """A reference to a large object stored in blob storage.

    This model represents metadata about objects stored in external blob storage,
    allowing workflows to pass references to large payloads without exceeding
    Temporal's message size limits.
    """

    uri: str = Field(description="The unique URI of the blob in storage.")
    content_type: str = Field(default="application/octet-stream", description="MIME type of the stored object.")
    size_bytes: int = Field(description="Size of the object in bytes.")

    # Optional metadata for better tracking and management
    key: str | None = Field(default=None, description="The storage key/path used to store the blob.")
    created_at: datetime | None = Field(default=None, description="When the blob was created in storage.")
    expires_at: datetime | None = Field(default=None, description="When the blob expires and should be cleaned up.")
