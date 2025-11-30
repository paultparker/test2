from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.models import AgentResponse, Plan, Step

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@patch("app.main.agent.run")
def test_chat_endpoint(mock_run):
    # Mock the agent response
    mock_response = AgentResponse(
        query="Test Query",
        plan=Plan(steps=[Step(step_number=1, description="Test Step", tool_name="test_tool", result="success")]),
        final_answer="This is a test answer.",
        verification_status="verified"
    )
    mock_run.return_value = mock_response

    response = client.post("/chat", json={"query": "Test Query"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "Test Query"
    assert data["final_answer"] == "This is a test answer."
    assert data["verification_status"] == "verified"
    assert len(data["plan"]["steps"]) == 1

@patch("app.main.agent.run")
def test_chat_endpoint_error(mock_run):
    # Mock an exception
    mock_run.side_effect = Exception("Agent failed")

    response = client.post("/chat", json={"query": "Crash me"})
    
    assert response.status_code == 500
    assert "Agent failed" in response.json()["detail"]
