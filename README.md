# Relationship Manager Co-Pilot

A bank-style agentic co-pilot designed to assist Relationship Managers (RMs) by looking up account details, searching knowledge bases, and retrieving CRM notes. Built with Python, FastAPI, and OpenAI.

## Features

- **Agentic Loop**: Implements a Planner -> Executor -> Verifier architecture.
  - **Planner**: Decomposes complex user queries into a step-by-step plan.
  - **Executor**: Executes the plan using available tools.
  - **Verifier**: Validates that the gathered information answers the user's request.
- **Simulated Tools**:
  - `account_lookup`: Retrieve account balances and details.
  - `kb_search`: Search internal knowledge base articles.
  - `crm_notes`: Access client meeting notes and preferences.
- **FastAPI Backend**: Exposes a RESTful API for agent interaction.

## Project Structure

```
.
├── app/
│   ├── agent/
│   │   ├── core.py       # Main agent loop logic
│   │   ├── llm.py        # OpenAI API wrapper
│   │   ├── prompts.py    # System prompts
│   │   └── tools.py      # Simulated tool implementations
│   ├── main.py           # FastAPI entry point
│   └── models.py         # Pydantic data models
├── tests/
│   ├── test_agent_mock.py    # Unit tests for agent loop
│   ├── test_api.py           # Integration tests for API
│   ├── test_e2e_scenarios.py # End-to-end scenarios
│   └── test_tools.py         # Unit tests for tools
├── requirements.txt
└── verify_real_llm.py    # Script to verify with real OpenAI API
```

## Setup

1. **Clone the repository**:

    ```bash
    git clone https://github.com/paultparker/test2.git
    cd test2
    ```

2. **Create a virtual environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Environment**:
    Create a `.env` file in the root directory and add your OpenAI API key:

    ```
    OPENAI_API_KEY=sk-your-api-key-here
    ```

## Usage

1. **Start the Server**:

    ```bash
    uvicorn app.main:app --reload
    ```

2. **Query the Agent**:
    You can use `curl` or any API client (like Postman).

    ```bash
    curl -X POST "http://localhost:8000/chat" \
         -H "Content-Type: application/json" \
         -d '{"query": "What is the balance of account ACC-123?"}'
    ```

    **Example Response**:

    ```json
    {
      "query": "What is the balance of account ACC-123?",
      "plan": { ... },
      "final_answer": "The balance of account ACC-123 is $15,000.00.",
      "verification_status": "verified"
    }
    ```

## Testing

Run the automated test suite:

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest test_e2e_scenarios.py
```
