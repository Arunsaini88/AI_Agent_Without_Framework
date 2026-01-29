import json


class Agent:
    def __init__(self, llm, tool_registry, max_steps = 5):
        self.llm = llm
        self.tool_registry = tool_registry
        self.history = []
        self.max_steps = max_steps

    def run(self, user_input: str):
        self.history.append({"role":"user", "content": user_input})

        for step in range(self.max_steps):
            # Get LLM decision
            llm_output = self.llm.generate(self.history)
            action = json.loads(llm_output)

            if action["action"] == "tool":
                # Recort the thought process
                self.history.append(
                    {"role": " assistent", "content": llm_output}
                )

                # Execute the tool
                tool = self.tool_registry.get(action["tool_name"])
                result = tool(**action["args"])

                # Record the result
                observation = f"Tool {tool.name} returned: {result}"

                self.history.append(
                    {"role": "tool", "tool_name": tool.name, "tool_response": result}
                )

                continue

            if action["action"] == "final":
                self.history.append(
                    {"role": "assistent", "content": llm_output}
                )

                return action["answer"]
            
        raise RuntimeError("Agent did not terminater within max_steps")
