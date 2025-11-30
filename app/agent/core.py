import json
from typing import Dict, Any
from app.agent.llm import call_llm
from app.agent.prompts import PLANNER_SYSTEM_PROMPT, VERIFIER_SYSTEM_PROMPT, FINAL_ANSWER_PROMPT
from app.agent.tools import AVAILABLE_TOOLS
from app.models import Plan, Step, AgentResponse
import logging

logger = logging.getLogger(__name__)

def parse_json_response(response: str) -> Dict[str, Any]:
    """Helper to parse JSON from LLM response, handling potential markdown blocks."""
    try:
        clean_response = response.strip()
        if clean_response.startswith("```json"):
            clean_response = clean_response.split("```json")[1]
        if clean_response.endswith("```"):
            clean_response = clean_response.rsplit("```", 1)[0]
        return json.loads(clean_response)
    except Exception as e:
        logger.error(f"Failed to parse JSON: {response}")
        return {}

class AgentCore:
    def __init__(self):
        self.tools = AVAILABLE_TOOLS

    def plan(self, query: str) -> Plan:
        logger.info(f"Planning for query: {query}")
        messages = [
            {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
        response = call_llm(messages)
        logger.debug(f"Planner raw response: {response}")
        plan_data = parse_json_response(response)
        
        steps = []
        if "steps" in plan_data:
            for s in plan_data["steps"]:
                steps.append(Step(**s))
        
        logger.info(f"Generated plan with {len(steps)} steps")
        return Plan(steps=steps)

    def execute(self, plan: Plan) -> Plan:
        logger.info("Starting plan execution")
        for step in plan.steps:
            if step.tool_name and step.tool_name in self.tools:
                logger.info(f"Executing step {step.step_number}: {step.tool_name}")
                tool_func = self.tools[step.tool_name]
                try:
                    # Execute tool
                    result = tool_func(**step.tool_args)
                    step.result = result
                    logger.info(f"Tool {step.tool_name} success")
                except Exception as e:
                    error_msg = f"Error executing tool: {str(e)}"
                    step.result = error_msg
                    logger.error(error_msg)
            else:
                step.result = "No tool execution needed or tool not found."
        return plan

    def verify(self, query: str, plan: Plan) -> str:
        # Convert plan with results to string for verifier
        plan_str = json.dumps([s.model_dump() for s in plan.steps], indent=2)
        
        messages = [
            {"role": "system", "content": VERIFIER_SYSTEM_PROMPT},
            {"role": "user", "content": f"Query: {query}\n\nExecuted Plan:\n{plan_str}"}
        ]
        response = call_llm(messages)
        verification_data = parse_json_response(response)
        return verification_data.get("status", "unknown")

    def generate_final_answer(self, query: str, plan: Plan) -> str:
        plan_str = json.dumps([s.model_dump() for s in plan.steps], indent=2)
        messages = [
            {"role": "system", "content": FINAL_ANSWER_PROMPT},
            {"role": "user", "content": f"Query: {query}\n\nInformation Gathered:\n{plan_str}"}
        ]
        return call_llm(messages)

    def run(self, query: str) -> AgentResponse:
        # 1. Plan
        plan = self.plan(query)
        
        # 2. Execute
        executed_plan = self.execute(plan)
        
        # 3. Verify
        verification_status = self.verify(query, executed_plan)
        
        # 4. Final Answer
        final_answer = self.generate_final_answer(query, executed_plan)
        
        return AgentResponse(
            query=query,
            plan=executed_plan,
            final_answer=final_answer,
            verification_status=verification_status
        )
