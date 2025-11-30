import unittest
from unittest.mock import patch
from app.agent.core import AgentCore
from app.models import Plan, Step

class TestAgentCore(unittest.TestCase):
    @patch('app.agent.core.call_llm')
    def test_agent_loop(self, mock_llm):
        # Mock Planner Response
        planner_response = """
        {
            "steps": [
                {
                    "step_number": 1,
                    "description": "Look up account details",
                    "tool_name": "account_lookup",
                    "tool_args": {"account_id": "ACC-123"}
                }
            ]
        }
        """
        
        # Mock Verifier Response
        verifier_response = """
        {
            "status": "verified",
            "reason": "Account details found."
        }
        """
        
        # Mock Final Answer
        final_answer = "The balance is $15,000."
        
        # Set side_effects for the 3 calls: Plan, Verify, Final Answer
        mock_llm.side_effect = [planner_response, verifier_response, final_answer]
        
        agent = AgentCore()
        response = agent.run("Check balance for ACC-123")
        
        # Assertions
        self.assertEqual(len(response.plan.steps), 1)
        self.assertEqual(response.plan.steps[0].tool_name, "account_lookup")
        self.assertIn("Alice Smith", response.plan.steps[0].result) # Check if tool actually ran and got real mock data
        self.assertEqual(response.verification_status, "verified")
        self.assertEqual(response.final_answer, "The balance is $15,000.")
        print("Agent Loop Test Passed!")

if __name__ == '__main__':
    unittest.main()
