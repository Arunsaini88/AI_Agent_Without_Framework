from pydantic import BaseModel
from typing import Literal, Union
from tool_registry import ToolRegistry
from tool_class import Tool
from schemas import ToolAddArgs, ToolMultplyArgs
from tools import add, multiply


registry = ToolRegistry()

registry.register(
    Tool(
        name = "add",
        description = "Add two numbers",
        input_schema = ToolAddArgs,
        output_schema = {"result": "int"},
        func = add,
    )
)

registry.register(
    Tool(
        name = "multiply",
        description = "Multiply two numbers",
        input_schema = ToolMultplyArgs,
        output_schema = {"result": "int"},
        func = multiply,
    )
)

# Get type-safe tool names and arguments

ToolNameLiteral = registry.get_tool_names()
ToolArgsUnion = registry.get_tool_call_args_type()


class ToolCall(BaseModel):
    action : Literal["tool"]
    thought : str
    tool_name: ToolNameLiteral
    args : ToolArgsUnion

class FinalAnswer(BaseModel):
    action: Literal['final']
    answer: str

LLMResponse = Union[ToolCall, FinalAnswer]
