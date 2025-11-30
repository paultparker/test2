from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ChatRequest(BaseModel):
    query: str

class Step(BaseModel):
    step_number: int
    description: str
    tool_name: Optional[str] = None
    tool_args: Optional[Dict[str, Any]] = None
    result: Optional[str] = None

class Plan(BaseModel):
    steps: List[Step]

class AgentResponse(BaseModel):
    query: str
    plan: Plan
    final_answer: str
    verification_status: str  # "verified", "failed", "unknown"
