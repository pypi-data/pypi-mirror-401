import dataclasses
from contextlib import contextmanager
from contextvars import ContextVar

from openai.types.chat import ChatCompletionMessageToolCall

from functioncalming.models import ToolCallOutcome
from functioncalming.utils import OpenAIFunction


@dataclasses.dataclass
class CalmContext:
    tool_call: ChatCompletionMessageToolCall
    openai_function: OpenAIFunction
    parallel_tool_calls: list[ChatCompletionMessageToolCall]
    parallel_tool_call_outcomes: dict[str, ToolCallOutcome]

calm_context: ContextVar[CalmContext | None] = ContextVar("calm_context", default=None)

@contextmanager
def set_calm_context(
        tool_call: ChatCompletionMessageToolCall,
        openai_function: OpenAIFunction,
        parallel_tool_calls: list[ChatCompletionMessageToolCall],
        parallel_tool_call_outcomes: dict[str, ToolCallOutcome]
):
    token = calm_context.set(
        CalmContext(
            tool_call=tool_call,
            openai_function=openai_function,
            parallel_tool_calls=parallel_tool_calls,
            parallel_tool_call_outcomes=parallel_tool_call_outcomes
        )
    )
    try:
        yield
    finally:
        calm_context.reset(token)

