from google import genai
from agent_orchestrator import Agent
from llm_wrapper import GeminiLLM
from registry import registry
# Initialize the client (you'll need  your API key)
client  = genai.Client(api_key = "AIzaSyBtpnyCeBwXGPFD5WDxMEfNkhxH0EDpbew")
#  create llm and Agent

llm = GeminiLLM(client, registry)

agent = Agent(llm, registry)

def chat_with_agent(agent: Agent):
    print("Welcome ! Type 'exit' to quit.\\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break
        try:
            response = agent.run(user_input)
            print(f"Answer: {response}" )
        
        except RuntimeError as e:
            print(f"Agent error: {e}")

        except Exception as e:
            print(f"Unexpected error: {e}")

# Start Chatting

chat_with_agent(agent)