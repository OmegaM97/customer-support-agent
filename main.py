from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from agents.triage_agent import triage_agent

from agents.specialized_agents import (
    billing_agent,
    technical_agent,
    feature_request_agent,
    knowledge_agent,
    account_management_agent
)

from agents.escalation_agent import (
    escalation_agent
)

from agents.response_agent import (
    response_agent
)

from agents.save_to_db_agent import (
    save_to_db_agent
)

from persistence import init_database


class SupportState(TypedDict):

    ticket_id: str
    customer_id: str
    message: str

    category: str

    tool_result: dict

    resolution: str
    confidence: float

    escalation_required: bool

    escalation_details: dict

    final_response: str


def route_ticket(state):

    return state["category"]


def route_escalation(state):

    if state["escalation_required"]:
        return "escalate"

    return "respond"


builder = StateGraph(
    SupportState
)


builder.add_node(
    "triage",
    triage_agent
)

builder.add_node(
    "billing",
    billing_agent
)

builder.add_node(
    "technical",
    technical_agent
)

builder.add_node(
    "feature_request",
    feature_request_agent
)

builder.add_node(
    "knowledge",
    knowledge_agent
)

builder.add_node(
    "account_management",
    account_management_agent
)

builder.add_node(
    "escalation",
    escalation_agent
)

builder.add_node(
    "response",
    response_agent
)

builder.add_node(
    "save_to_db",
    save_to_db_agent
)


builder.add_edge(
    START,
    "triage"
)


builder.add_conditional_edges(
    "triage",
    route_ticket,
    {
        "Billing": "billing",
        "Technical Issue": "technical",
        "Feature Request": "feature_request",
        "General Inquiry": "knowledge",
        "Account Management": "account_management"
    }
)


builder.add_conditional_edges(
    "billing",
    route_escalation,
    {
        "escalate": "escalation",
        "respond": "response"
    }
)

builder.add_conditional_edges(
    "technical",
    route_escalation,
    {
        "escalate": "escalation",
        "respond": "response"
    }
)

builder.add_conditional_edges(
    "feature_request",
    route_escalation,
    {
        "escalate": "escalation",
        "respond": "response"
    }
)

builder.add_conditional_edges(
    "knowledge",
    route_escalation,
    {
        "escalate": "escalation",
        "respond": "response"
    }
)

builder.add_conditional_edges(
    "account_management",
    route_escalation,
    {
        "escalate": "escalation",
        "respond": "response"
    }
)


builder.add_edge(
    "escalation",
    "response"
)

builder.add_edge(
    "response",
    "save_to_db"
)

builder.add_edge(
    "save_to_db",
    END
)


graph = builder.compile()


if __name__ == "__main__":

    # Initialize database
    init_database()

    initial_state = {
        "ticket_id": "T-1001",
        "customer_id": "C-500",
        "message": "I was charged twice for my subscription."
    }

    result = graph.invoke(
        initial_state
    )

    print("\n===================")
    print("FINAL STATE")
    print("===================")

    print(result)