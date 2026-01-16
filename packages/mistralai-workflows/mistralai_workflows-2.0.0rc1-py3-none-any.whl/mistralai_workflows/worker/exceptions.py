from temporalio.exceptions import ActivityError as TemporalActivityError
from temporalio.exceptions import ApplicationError as TemporalApplicationError


class WorkflowError(TemporalApplicationError):
    """Base exception for all Mistral Workflows errors."""

    pass


class NotInTemporalContextError(WorkflowError):
    """Raised when code is executed outside of a Temporal workflow or activity context."""

    def __init__(self) -> None:
        super().__init__("Not in a Temporal context. This function must be called from within a workflow or activity.")


ActivityError = TemporalActivityError
