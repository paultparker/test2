from app.agent.core import AgentCore
from dotenv import load_dotenv
import json

load_dotenv()

def debug_case_2():
    agent = AgentCore()
    query = "Find KB articles about wire transfers."
    print(f"Query: {query}")
    
    response = agent.run(query)
    
    print("\n--- Plan ---")
    for step in response.plan.steps:
        print(f"Step {step.step_number}: {step.tool_name}")
        print(f"Args: {step.tool_args}")
        print(f"Result: {step.result}")
        
    print("\n--- Final Answer ---")
    print(response.final_answer)

if __name__ == "__main__":
    debug_case_2()
