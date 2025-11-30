from fastapi import FastAPI, HTTPException
from app.models import ChatRequest, AgentResponse
from app.agent.core import AgentCore
import uvicorn

import uvicorn
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Relationship Manager Co-Pilot")
agent = AgentCore()

@app.post("/chat", response_model=AgentResponse)
async def chat(request: ChatRequest):
    logger.info(f"Received chat request: {request.query}")
    try:
        response = agent.run(request.query)
        logger.info(f"Agent finished. Verification: {response.verification_status}")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
