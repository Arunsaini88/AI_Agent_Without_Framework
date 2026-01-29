from typing import Union, Literal, Dict, List, Any
from tool_class import Tool
from pydantic import BaseModel

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
    def register(self, tool: Tool):
        self.tools[tool.name] = tool
    def get(self, name: str) -> Tool:
        if name not in self.tools.keys():
            raise ValueError(f"Tool '{name}' not found")
        return self.tools[name]
    def list_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.input_schema.model_json_schema(),
            }
            for tool in self.tools.values()
        ]
    def get_tool_call_args_type(self) -> Union[BaseModel]:
        input_args_models = [tool.input_schema for tool in self.tools.values()]
        tool_call_args = Union[tuple(input_args_models)]
        return tool_call_args
    def get_tool_names(self) -> Literal[None]:
        return Literal[*self.tools.keys()]