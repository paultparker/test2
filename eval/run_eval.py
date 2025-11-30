import json
import os
import sys
import asyncio
from typing import List, Dict
from dotenv import load_dotenv

# Add project root to path so we can import app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.agent.core import AgentCore
from app.agent.llm import call_llm

load_dotenv()

def evaluate_fact_recall(query: str, final_answer: str, expected_facts: List[str]) -> Dict:
    """
    Uses LLM-as-a-judge to check if expected facts are present in the answer.
    """
    facts_str = "\n".join([f"- {fact}" for fact in expected_facts])
    prompt = f"""
    You are an impartial judge evaluating an AI agent's response.
    
    User Query: {query}
    Agent Response: {final_answer}
    
    Expected Facts:
    {facts_str}
    
    Task: Check if the Agent Response contains the information from the Expected Facts.
    For each fact, determine if it is present (Pass) or missing (Fail).
    
    Output JSON format:
    {{
        "results": [
            {{"fact": "fact text", "status": "Pass"}},
            {{"fact": "fact text", "status": "Fail"}}
        ],
        "score": <number of passed facts / total facts>
    }}
    """
    
    messages = [{"role": "user", "content": prompt}]
    response = call_llm(messages)
    
    try:
        # Basic cleanup for JSON parsing
        clean_response = response.strip()
        if clean_response.startswith("```json"):
            clean_response = clean_response.split("```json")[1]
        if clean_response.endswith("```"):
            clean_response = clean_response.rsplit("```", 1)[0]
        return json.loads(clean_response)
    except:
        return {"results": [], "score": 0.0, "error": "Failed to parse LLM judgment"}

def run_eval():
    # Load dataset
    with open("eval/dataset.json", "r") as f:
        dataset = json.load(f)
    
    agent = AgentCore()
    results = []
    
    print(f"Starting evaluation of {len(dataset)} cases...\n")
    
    for case in dataset:
        print(f"Running Case: {case['id']}")
        
        # Run Agent
        try:
            response = agent.run(case["query"])
            
            # 1. Tool Usage Metric
            executed_tools = [s.tool_name for s in response.plan.steps if s.tool_name]
            expected_tools = case["expected_tools"]
            
            # Simple set match for tools (ignoring order/duplicates for now)
            tool_match = set(expected_tools).issubset(set(executed_tools))
            
            # 2. Fact Recall Metric
            fact_eval = evaluate_fact_recall(case["query"], response.final_answer, case["expected_facts"])
            
            case_result = {
                "id": case["id"],
                "tool_match": tool_match,
                "fact_score": fact_eval.get("score", 0),
                "details": fact_eval
            }
            results.append(case_result)
            
            print(f"  -> Tools: {'OK' if tool_match else 'MISSING'} ({executed_tools})")
            print(f"  -> Facts: {fact_eval.get('score', 0):.2f}")
            
        except Exception as e:
            print(f"  -> Error: {e}")
            results.append({"id": case["id"], "error": str(e)})
            
    # Summary
    print("\n--- Evaluation Summary ---")
    total_cases = len(dataset)
    passed_tools = sum(1 for r in results if r.get("tool_match"))
    avg_fact_score = sum(r.get("fact_score", 0) for r in results) / total_cases if total_cases > 0 else 0
    
    print(f"Total Cases: {total_cases}")
    print(f"Tool Usage Accuracy: {passed_tools/total_cases:.2%}")
    print(f"Average Fact Recall: {avg_fact_score:.2%}")
    
    # Save detailed results
    with open("eval/results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nDetailed results saved to eval/results.json")

if __name__ == "__main__":
    run_eval()
