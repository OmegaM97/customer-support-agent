from langchain_groq import ChatGroq


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


def response_agent(state):

    escalation_details = state.get(
        "escalation_details",
        {}
    )

    prompt = f"""
You are a customer support response agent.

Generate the final customer-facing response.

Ticket:
{state["message"]}

Category:
{state["category"]}

Resolution:
{state["resolution"]}

Escalation Required:
{state["escalation_required"]}

Escalation Details:
{escalation_details}

Human Approval for Escalation:
{"yes" if state.get("human_approved") else "no"}

Generate a professional customer response.

Mention:

1. Issue category
2. Resolution summary
3. Any next actions
4. Escalation status
5. only escalted if both escalation_required and human_approved are true
6. and dont add those your name, company name thing just good response
"""

    response = llm.invoke(prompt)

    state["final_response"] = (
        response.content
    )

    print("\n=== FINAL RESPONSE ===")
    print(state["final_response"])

    return state