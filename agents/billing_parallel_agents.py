from pydantic import BaseModel

from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser

from tools.specialized_agents_tools import (
    lookup_subscription,
    lookup_payment_history,
    lookup_refund_status
)


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


class BillingResolution(BaseModel):
    resolution: str
    confidence: float
    escalation_required: bool


resolution_parser = JsonOutputParser(
    pydantic_object=BillingResolution
)


def billing_router(state):

    return {}


def billing_subscription_agent(state):

    result = lookup_subscription(
        state["customer_id"]
    )

    print("\n=== BILLING SUBSCRIPTION CHECK ===")
    print(result)

    return {
        "billing_results": [
            {
                "type": "subscription",
                "data": result
            }
        ]
    }


def billing_payment_agent(state):

    result = lookup_payment_history(
        state["customer_id"]
    )

    print("\n=== BILLING PAYMENT CHECK ===")
    print(result)

    return {
        "billing_results": [
            {
                "type": "payment",
                "data": result
            }
        ]
    }


def billing_refund_agent(state):

    result = lookup_refund_status(
        state["customer_id"]
    )

    print("\n=== BILLING REFUND CHECK ===")
    print(result)

    return {
        "billing_results": [
            {
                "type": "refund",
                "data": result
            }
        ]
    }


def billing_merge_agent(state):

    subscription = {}
    payment = {}
    refund = {}

    for item in state.get(
        "billing_results",
        []
    ):

        if item["type"] == "subscription":
            subscription = item["data"]

        elif item["type"] == "payment":
            payment = item["data"]

        elif item["type"] == "refund":
            refund = item["data"]

    prompt = f"""
You are a Billing Resolution Agent.

Customer Ticket:
{state["message"]}

Subscription Investigation:
{subscription}

Payment Investigation:
{payment}

Refund Investigation:
{refund}

Analyze all investigations.

Provide:

- resolution
- confidence
- escalation_required

Escalate when:

- duplicate charges exist
- refund approval is needed
- money is involved
- billing disputes exist

{resolution_parser.get_format_instructions()}
"""

    response = llm.invoke(
        prompt
    )

    result = resolution_parser.parse(
        response.content
    )

    print("\n=== BILLING MERGE ===")
    print(result["resolution"])

    return {
        "resolution": result["resolution"],
        "confidence": result["confidence"],
        "escalation_required": result[
            "escalation_required"
        ]
    }