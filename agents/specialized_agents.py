from pydantic import BaseModel

from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser

from tools.specialized_agents_tools import (
    lookup_subscription,
    lookup_payment_history,
    lookup_refund_status,

    search_known_issues,
    lookup_system_status,

    feature_catalog_lookup,
    roadmap_lookup,

    search_knowledge_base,
    faq_lookup,

    lookup_account,
    lookup_login_history
)


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


class ToolDecision(BaseModel):
    tool_name: str
    argument: str


class AgentResolution(BaseModel):
    resolution: str
    confidence: float
    escalation_required: bool


tool_parser = JsonOutputParser(
    pydantic_object=ToolDecision
)

resolution_parser = JsonOutputParser(
    pydantic_object=AgentResolution
)


TOOLS = {

    # Billing
    "lookup_subscription": lookup_subscription,
    "lookup_payment_history": lookup_payment_history,
    "lookup_refund_status": lookup_refund_status,

    # Technical
    "search_known_issues": search_known_issues,
    "lookup_system_status": lookup_system_status,

    # Feature Request
    "feature_catalog_lookup": feature_catalog_lookup,
    "roadmap_lookup": roadmap_lookup,

    # General Inquiry
    "search_knowledge_base": search_knowledge_base,
    "faq_lookup": faq_lookup,

    # Account Management
    "lookup_account": lookup_account,
    "lookup_login_history": lookup_login_history
}


def run_agent(
    state,
    agent_name,
    available_tools
):

    tool_prompt = f"""
You are the {agent_name}.

Customer Ticket:
{state["message"]}

Customer ID:
{state["customer_id"]}

Available Tools:
{available_tools}

Choose the SINGLE best tool to use.

Rules:

- Use customer_id when a customer lookup tool is needed.
- Use the ticket message when an issue analysis tool is needed.
- Always choose exactly one tool.
- Return the tool name and argument.

{tool_parser.get_format_instructions()}
"""

    tool_response = llm.invoke(
        tool_prompt
    )

    tool_decision = tool_parser.parse(
        tool_response.content
    )

    selected_tool = tool_decision["tool_name"]

    argument = tool_decision["argument"]

    tool_result = TOOLS[selected_tool](
        argument
    )

    state["selected_tool"] = selected_tool
    state["tool_result"] = tool_result

    resolution_prompt = f"""
You are the {agent_name}.

Customer Ticket:
{state["message"]}

Selected Tool:
{selected_tool}

Tool Result:
{tool_result}

Analyze the issue.

Provide:

- resolution
- confidence between 0 and 1
- escalation_required

Escalation should be true when:

- issue is complex
- issue cannot be solved automatically
- information is missing
- security concerns exist
- anything involving money
- account changes
- account recovery
- refunds
- billing disputes
- suspicious account activity

{resolution_parser.get_format_instructions()}
"""

    resolution_response = llm.invoke(
        resolution_prompt
    )

    final_response = resolution_parser.parse(
        resolution_response.content
    )

    state["resolution"] = final_response["resolution"]
    state["confidence"] = final_response["confidence"]
    state["escalation_required"] = (
        final_response["escalation_required"]
    )

    print(f"\n=== {agent_name.upper()} ===")

    print("\nSelected Tool:")
    print(selected_tool)

    print("\nTool Result:")
    print(tool_result)

    print("\nResolution:")
    print(state["resolution"])

    print("\nConfidence:")
    print(state["confidence"])

    print("\nEscalation Required:")
    print(state["escalation_required"])

    return state


def billing_agent(state):

    return run_agent(
        state,
        "Billing Agent",
        [
            "lookup_subscription",
            "lookup_payment_history",
            "lookup_refund_status"
        ]
    )


def technical_agent(state):

    return run_agent(
        state,
        "Technical Agent",
        [
            "search_known_issues",
            "lookup_system_status"
        ]
    )


def feature_request_agent(state):

    return run_agent(
        state,
        "Feature Request Agent",
        [
            "feature_catalog_lookup",
            "roadmap_lookup"
        ]
    )


def knowledge_agent(state):

    return run_agent(
        state,
        "Knowledge Agent",
        [
            "search_knowledge_base",
            "faq_lookup"
        ]
    )


def account_management_agent(state):

    return run_agent(
        state,
        "Account Management Agent",
        [
            "lookup_account",
            "lookup_login_history"
        ]
    )