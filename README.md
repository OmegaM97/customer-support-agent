# Customer Support Agent

This is a LangGraph-based customer support workflow that classifies tickets, routes them to the right agent, escalates when needed, generates a final reply, and saves the result to SQLite.

## System Architecture

- [main.py](main.py) builds the graph and runs the app.
- `agents/` contains the workflow nodes.
- `tools/` contains the mock lookup functions.
- [persistence.py](persistence.py) saves completed tickets in SQLite.

## Agent Responsibilities

- `triage_agent.py`: classifies the ticket as Billing, Technical Issue, Feature Request, General Inquiry, or Account Management.
- `billing_parallel_agents.py`: runs billing checks in parallel and merges the result.
- `specialized_agents.py`: handles technical, feature, knowledge, and account cases.
- `human_approval_agent.py`: asks for approval when escalation is required.
- `escalation_agent.py`: sends the ticket to Tier 2 support.
- `response_agent.py`: writes the final customer response.
- `save_to_db_agent.py`: stores the finished workflow state.

## State Design

The shared state in [main.py](main.py) includes:

- `ticket_id`
- `customer_id`
- `message`
- `category`
- `selected_tool`
- `tool_result`
- `billing_results`
- `resolution`
- `confidence`
- `escalation_required`
- `human_approved`
- `escalation_details`
- `final_response`

## Routing Logic

- `triage` sends the ticket to the correct branch.
- Billing goes through `billing_subscription`, `billing_payment`, and `billing_refund`, then `billing_merge`.
- Other categories go to a single specialized agent.
- If `escalation_required` is true, the ticket goes to human approval.
- Approved escalations go to `escalation`, then `response`, then `save_to_db`.

## Tool Integration

The workflow uses simple mock tools from [tools/specialized_agents_tools.py](tools/specialized_agents_tools.py):

- Billing: `lookup_subscription`, `lookup_payment_history`, `lookup_refund_status`
- Technical: `search_known_issues`, `lookup_system_status`
- Feature: `feature_catalog_lookup`, `roadmap_lookup`
- Knowledge: `search_knowledge_base`, `faq_lookup`
- Account: `lookup_account`, `lookup_login_history`
- Escalation: `telegram_tool`

## Persistence Strategy

[`persistence.py`](persistence.py) creates `db/support.db` and stores each completed ticket in a `tickets` table.

## Run

```bash
python main.py
```

Make sure `GROQ_API_KEY` is set in `.env` before running.

## Sample Executions

### 1. Billing Issue

Input:

```python
initial_state = {
    "ticket_id": "T-1001",
    "customer_id": "C-500",
    "message": "I was charged twice for my subscription.",
    "billing_results": []
}
```

Path:

`triage -> billing_router -> billing_subscription + billing_payment + billing_refund -> billing_merge -> human_approval -> escalation -> response -> save_to_db`

Final output:

Refund the duplicate charge of $29.99 and confirm cancellation of the duplicate payment. The case was escalated to Tier 2 Support.

### 2. Technical Issue

Input:

```python
initial_state = {
    "ticket_id": "T-1003",
    "customer_id": "C-501",
    "message": "The mobile app crashes every time I try to upload a file.",
    "billing_results": []
}
```

Path:

`triage -> technical -> response -> save_to_db`

Final output:

Clear the app cache and reinstall the mobile app to resolve the crash during file upload. No escalation is required.

### 3. Feature Request

Input:

```python
initial_state = {
    "ticket_id": "T-1004",
    "customer_id": "C-502",
    "message": "It would be great if the platform supported dark mode.",
    "billing_results": []
}
```

Path:

`triage -> feature_request -> response -> save_to_db`

Final output:

Dark mode is on the roadmap for Q4 2026. No escalation is needed.

### 4. General Inquiry

Input:

```python
initial_state = {
    "ticket_id": "T-1005",
    "customer_id": "C-503",
    "message": "What are your business hours and support availability?",
    "billing_results": []
}
```

Path:

`triage -> knowledge -> response -> save_to_db`

Final output:

Business hours are Monday to Friday, 9:00 AM to 5:00 PM Eastern Time. Support is available 24/7 via live chat and email.

### 5. Escalated Case

Input:

```python
initial_state = {
    "ticket_id": "T-1006",
    "customer_id": "C-504",
    "message": "I need to update the email address associated with my account.",
    "billing_results": []
}
```

Path:

`triage -> account_management -> human_approval -> escalation -> response -> save_to_db`

Final output:

Update your email in Settings > Email, then confirm through the verification link. The request was escalated to Tier 2 Support.
