from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import json


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


def triage_agent(state):

    message = state["message"]

    prompt = f"""
You are a customer support triage agent.

Classify the customer ticket into exactly one category.

Possible categories:
- Billing
- Technical Issue
- Feature Request
- General Inquiry
- Account Management

Ticket:
{message}

Return ONLY valid JSON.

Example:
{{
    "category":"Billing"
}}
"""

    response = llm.invoke([HumanMessage(content=prompt)])

    result = json.loads(response.content)

    state["category"] = result["category"]

    print("\n=== TRIAGE ===")
    print(state["category"])

    return state