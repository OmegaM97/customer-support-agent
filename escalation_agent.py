from langchain_groq import ChatGroq


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


def create_escalation_ticket(
    ticket_id,
    reason
):
    """
    Mock escalation tool.

    Later:
    - Telegram
    - Email
    - Jira
    """

    return {
        "escalation_id": f"ESC-{ticket_id}",
        "status": "OPEN",
        "assigned_team": "Tier 2 Support",
        "reason": reason
    }


def escalation_agent(state):

    escalation_data = create_escalation_ticket(
        state["ticket_id"],
        state["resolution"]
    )

    state["escalation_details"] = escalation_data

    print("\n=== ESCALATION AGENT ===")
    print(escalation_data)

    return state