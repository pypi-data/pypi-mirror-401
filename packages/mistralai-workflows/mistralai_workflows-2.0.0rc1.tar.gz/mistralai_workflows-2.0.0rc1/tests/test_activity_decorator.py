import pytest
from pydantic import BaseModel, Field

from mistralai_workflows import activity
from mistralai_workflows.common.exceptions import ErrorCode, WorkflowsException


class ParamsModel(BaseModel):
    name: str = Field(description="Test name")
    count: int = Field(default=1)


class ResultModel(BaseModel):
    message: str
    success: bool = True


class TestActivityDecorator:
    def test_activity_not_async_raises_error(self) -> None:
        with pytest.raises(WorkflowsException, match="must be async function") as exc:

            @activity()
            def sync_activity(params: ParamsModel) -> ResultModel:
                return ResultModel(message="test")

        assert exc.value.code == ErrorCode.ACTIVITY_DEFINITION_ERROR

    def test_activity_with_primitive_param_works(self) -> None:
        @activity()
        async def valid_activity(params: str) -> ResultModel:
            return ResultModel(message=params)

        assert valid_activity is not None

    def test_activity_with_primitive_return_works(self) -> None:
        @activity()
        async def valid_activity(params: ParamsModel) -> str:
            return "test"

        assert valid_activity is not None

    def test_activity_on_class_raises_error(self) -> None:
        with pytest.raises(WorkflowsException, match="only supports module-level functions") as exc:

            @activity()
            class NotAFunction:
                pass

        assert exc.value.code == ErrorCode.ACTIVITY_NOT_MODULE_LEVEL
