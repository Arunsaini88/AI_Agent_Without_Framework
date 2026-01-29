import json
from google import genai
from google.genai import types
from registry import LLMResponse


class GeminiLLM:
    def __init__(self, client, tool_registry, model = "gemini-2.5-flash"):
        self.client = client
        self.model = model
        self.tool_registry = tool_registry
        self.system_instruction = self._create_system_instruction()


    def _create_system_instruction(self) -> str:
        tools_description = json.dumps(
            self.tool_registry.list_tools(),
            indent=2
        )

        system_prompt = """
        You are a conversational AI agent that can interact with external tools.
        CRITICAL RULES (MUST FOLLOW):
        - You are NOT allowed to perform operations internally that could be performed by an available tool.
        - If a tool exists that can perform any part of the task, you MUST use that tool.
        - You MUST NOT skip tools, even for simple or obvious steps.
        - You MUST NOT combine multiple operations into a single step unless a tool explicitly supports it.
        - You may ONLY produce a final answer when no available tool can further advance the task.
        TOOL USAGE RULES:
        - Each tool call must perform exactly ONE meaningful operation.
        - If the task requires multiple operations, you MUST call tools sequentially.
        - If multiple tools could apply, choose the most specific one.
        RESPONSE FORMAT (STRICT):
        - You MUST respond ONLY in valid JSON.
        - Never include explanations outside JSON.
        - You must choose exactly one action per response.
        Tool call format:
        {
        "action": "tool",
        "thought": "...",
        "tool_name": "...",
        "inputs": { ... }
        }
        Final answer format:
        {
        "action": "final",
        "answer": "..."
        }""" + "\\n\\nAvailable tools with description:\\n" + tools_description
        return system_prompt
    
    def _format_gemini_chat_history(self, history: list[dict]) -> list:
        formatted_history = []
        for message in history:
            if message["role"] == "user":
                formatted_history.append(types.Content(
                        role="user",
                        parts=[
                            types.Part.from_text(text=message["content"])
                        ]
                    )
                )
            if message["role"] == "assistant":
                formatted_history.append(types.Content(
                        role="model",
                        parts=[
                            types.Part.from_text(text=message["content"])
                        ]
                    )
                )
            if message["role"] == "tool":
                formatted_history.append(types.Content(
                        role="tool",
                        parts=[
                            types.Part.from_function_response(
                                name=message["tool_name"],
                                response={'result': message["tool_response"]},
                            )
                        ]
                    )
                )
        return formatted_history
    
    def generate(self, history: list[dict]) -> str:
        gemini_history_format = self._format_gemini_chat_history(history)
        response = self.client.models.generate_content(
            model=self.model,
            contents=gemini_history_format,
            config=types.GenerateContentConfig(
                temperature=0,
                response_mime_type="application/json",
                response_schema=LLMResponse,
                system_instruction=self.system_instruction,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
            ),
        )
        return response.text
    
