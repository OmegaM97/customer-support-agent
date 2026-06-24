import json

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from tools import (
    lookup_subscription,
    search_known_issues,
    feature_catalog_lookup,
    search_knowledge_base,
    lookup_account
)


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
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

You have access to one tool:

{tool_name}

Determine if the tool should be used.

Return ONLY JSON.

Example:
{{
    "use_tool": true,
    "argument": "C-500"
}}

or

{{
    "use_tool": false,
    "argument": ""
}}
"""

    tool_decision = llm.invoke(
        [HumanMessage(content=tool_prompt)]
    )

    tool_decision = json.loads(tool_decision.content)

    tool_result = {}

    if tool_decision["use_tool"]:

        argument = tool_decision["argument"]

        tool_result = TOOLS[tool_name](argument)

    state["tool_result"] = tool_result

    resolution_prompt = f"""
You are the {agent_name}.

Ticket:
{state["message"]}

Tool Result:
{tool_result}

Generate:

1. resolution
2. confidence between 0 and 1
3. escalation_required

Return ONLY JSON.

Example:

{{
    "resolution":"Refund initiated.",
    "confidence":0.92,
    "escalation_required":false
}}
"""

    final_response = llm.invoke(
        [HumanMessage(content=resolution_prompt)]
    )

    final_response = json.loads(
        final_response.content
    )

    state["resolution"] = final_response["resolution"]
    state["confidence"] = final_response["confidence"]
    state["escalation_required"] = final_response["escalation_required"]

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