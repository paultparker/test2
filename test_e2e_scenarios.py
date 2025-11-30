import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

# Helper to create mock LLM responses
def create_mock_llm_responses(plan_steps, verification_status="verified", final_answer="Done"):
    plan_json = json.dumps({"steps": plan_steps})
    verify_json = json.dumps({"status": verification_status, "reason": "checked"})
    return [plan_json, verify_json, final_answer]

@patch("app.agent.core.call_llm")
def test_e2e_account_lookup(mock_llm):
    """
    Scenario 1: Simple Account Lookup
    User: "What is the balance of ACC-456?"
    """
    # 1. Planner Output
    plan_steps = [{
        "step_number": 1,
        "description": "Lookup account ACC-456",
        "tool_name": "account_lookup",
        "tool_args": {"account_id": "ACC-456"}
    }]
    
    # Setup mock sequence: Plan -> Verify -> Final Answer
    mock_llm.side_effect = create_mock_llm_responses(
        plan_steps, 
        final_answer="The balance is $2,500.50."
    )

    response = client.post("/chat", json={"query": "What is the balance of ACC-456?"})
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify Plan
    assert len(data["plan"]["steps"]) == 1
    assert data["plan"]["steps"][0]["tool_name"] == "account_lookup"
    # Verify Tool Execution (Real tool should have run)
    assert "Bob Jones" in data["plan"]["steps"][0]["result"]
    # Verify Final Answer
    assert "2,500.50" in data["final_answer"]

@patch("app.agent.core.call_llm")
def test_e2e_multi_step_research(mock_llm):
    """
    Scenario 2: Multi-Step Research (CRM + KB)
    User: "Check CRM notes for Bob and find investment products."
    """
    # 1. Planner Output
    plan_steps = [
        {
            "step_number": 1,
            "description": "Get CRM notes for Bob",
            "tool_name": "crm_notes",
            "tool_args": {"client_name": "Bob"}
        },
        {
            "step_number": 2,
            "description": "Search KB for investment products",
            "tool_name": "kb_search",
            "tool_args": {"query": "investment"}
        }
    ]
    
    mock_llm.side_effect = create_mock_llm_responses(
        plan_steps, 
        final_answer="Bob is saving for a car. We offer ETFs and Mutual Funds."
    )

    response = client.post("/chat", json={"query": "Check CRM notes for Bob and find investment products."})
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify Plan
    assert len(data["plan"]["steps"]) == 2
    # Verify Tool 1
    assert data["plan"]["steps"][0]["tool_name"] == "crm_notes"
    assert "Saving for a new car" in data["plan"]["steps"][0]["result"]
    # Verify Tool 2
    assert data["plan"]["steps"][1]["tool_name"] == "kb_search"
    assert "ETFs" in data["plan"]["steps"][1]["result"]

@patch("app.agent.core.call_llm")
def test_e2e_tool_error_recovery(mock_llm):
    """
    Scenario 3: Tool Error / Recovery
    User: "Lookup account ACC-999" (Non-existent)
    """
    # 1. Planner Output
    plan_steps = [{
        "step_number": 1,
        "description": "Lookup account ACC-999",
        "tool_name": "account_lookup",
        "tool_args": {"account_id": "ACC-999"}
    }]
    
    mock_llm.side_effect = create_mock_llm_responses(
        plan_steps, 
        verification_status="failed", # Verifier might notice it failed, but we still get a response
        final_answer="Account ACC-999 was not found."
    )

    response = client.post("/chat", json={"query": "Lookup account ACC-999"})
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify Plan
    assert len(data["plan"]["steps"]) == 1
    # Verify Tool Execution
    assert "not found" in data["plan"]["steps"][0]["result"]
    # Verify Final Answer
    assert "not found" in data["final_answer"]
