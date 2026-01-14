import dataclasses

from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionMessageFunctionToolCall, \
    ChatCompletionToolMessageParam

from functioncalming.types import JsonCompatible


@dataclasses.dataclass
class StructuredOutputOutcome:
    success: bool
    raw_content: str
    result: JsonCompatible
    error: BaseException | None
    tool_name: str | None

    def to_response(self) -> ChatCompletionSystemMessageParam:
        from functioncalming.utils import serialize_openai_function_result
        if self.success:
            raise ValueError("Shouldn't need to call to_response on a successful structured response.")
        return ChatCompletionSystemMessageParam(
            role="system",
            content=f"Error: {serialize_openai_function_result(self.result)}"
        )

@dataclasses.dataclass
class ToolCallOutcome:
    success: bool
    tool_call_id: str
    raw_tool_call: ChatCompletionMessageFunctionToolCall
    result: JsonCompatible
    error: BaseException | None
    tool_name: str | None

    def to_response(self) -> ChatCompletionToolMessageParam:
        from functioncalming.utils import serialize_openai_function_result
        return ChatCompletionToolMessageParam(
            role="tool",
            tool_call_id=self.tool_call_id,
            content=serialize_openai_function_result(self.result)
        )