from typing import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph import START
from langgraph.graph import END

from triage_agent import triage_agent

from specialized_agents import (
    billing_agent,
    technical_agent,
    feature_request_agent,
    knowledge_agent,
    account_management_agent
)


class SupportState(TypedDict):

    ticket_id: str
    customer_id: str
    message: str

    category: str

    tool_result: dict

    resolution: str
    confidence: float

    escalation_required: bool


def route_ticket(state):

    return state["category"]


builder = StateGraph(SupportState)

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

builder.add_edge(
    "billing",
    END
)

builder.add_edge(
    "technical",
    END
)

builder.add_edge(
    "feature_request",
    END
)

builder.add_edge(
    "knowledge",
    END
)

builder.add_edge(
    "account_management",
    END
)

graph = builder.compile()


if __name__ == "__main__":

    initial_state = {
        "ticket_id": "T-1001",
        "customer_id": "C-500",
        "message": "I was charged twice for my subscription."
    }

    result = graph.invoke(
        initial_state
    )

    print("\n=== FINAL STATE ===")
    print(result)