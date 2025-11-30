import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
# Note: In a real app, you might want to handle missing keys more gracefully
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

def call_llm(messages: list, model: str = "gpt-4o") -> str:
    """
    Wrapper for calling OpenAI ChatCompletion.
    """
    if not client:
        # Fallback for demo purposes if no key is provided
        return "Error: OPENAI_API_KEY not found in environment variables."
        
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.0, # Deterministic for agents
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling LLM: {str(e)}"
