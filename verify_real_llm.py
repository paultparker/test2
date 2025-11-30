from app.agent.core import AgentCore
from dotenv import load_dotenv
import os

# Load env vars
load_dotenv()

def test_real_agent():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment.")
        return

    print(f"Testing with API Key: {api_key[:5]}... (masked)")
    
    agent = AgentCore()
    query = "What is the balance of account ACC-123?"
    print(f"\nQuery: {query}")
    
    try:
        response = agent.run(query)
        print("\n--- Agent Response ---")
        print(f"Final Answer: {response.final_answer}")
        print(f"Verification Status: {response.verification_status}")
        print("Plan Steps:")
        for step in response.plan.steps:
            print(f"  - {step.description} (Tool: {step.tool_name}) -> Result: {str(step.result)[:50]}...")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_real_agent()
