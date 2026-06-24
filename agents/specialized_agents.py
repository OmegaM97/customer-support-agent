from pydantic import BaseModel

from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser

from tools.specialized_agents_tools import (
    lookup_subscription,
    search_known_issues,
    feature_catalog_lookup,
    search_knowledge_base,
    lookup_account
)


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


class ToolDecision(BaseModel):
    use_tool: bool
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
    "lookup_subscription": lookup_subscription,
    "search_known_issues": search_known_issues,
    "feature_catalog_lookup": feature_catalog_lookup,
    "search_knowledge_base": search_knowledge_base,
    "lookup_account": lookup_account
}


def run_agent(
    state,
    agent_name,
    tool_name
):

    tool_prompt = f"""
You are the {agent_name}.

Ticket:
{state["message"]}

Customer ID:
{state["customer_id"]}

Available Tool:
{tool_name}

Decide whether the tool should be used.

If the tool should be used:
- use_tool must be true
- provide the correct argument

If the tool should not be used:
- use_tool must be false
- argument must be empty

{tool_parser.get_format_instructions()}
"""

    tool_response = llm.invoke(
        tool_prompt
    )

    tool_decision = tool_parser.parse(
        tool_response.content
    )

    tool_result = {}

    if tool_decision["use_tool"]:

        tool_result = TOOLS[tool_name](
            tool_decision["argument"]
        )

    state["tool_result"] = tool_result

    resolution_prompt = f"""
You are the {agent_name}.

Customer Ticket:
{state["message"]}

Tool Result:
{tool_result}

Analyze the issue.

Provide:

- resolution
- confidence between 0 and 1
- escalation_required

Escalation should be true if:

- issue is complex
- issue cannot be solved automatically
- information is missing
- security concerns exist
-anything belong to money, account, changing data should be escalated

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
    print("Tool Result:")
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
        "lookup_subscription"
    )


def technical_agent(state):

    return run_agent(
        state,
        "Technical Agent",
        "search_known_issues"
    )


def feature_request_agent(state):

    return run_agent(
        state,
        "Feature Request Agent",
        "feature_catalog_lookup"
    )


def knowledge_agent(state):

    return run_agent(
        state,
        "Knowledge Agent",
        "search_knowledge_base"
    )


def account_management_agent(state):

    return run_agent(
        state,
        "Account Management Agent",
        "lookup_account"
    )