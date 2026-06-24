from tools.telegram_tool import telegram_tool

def escalation_agent(state):

    escalation_data = telegram_tool(
        state["ticket_id"],
        state["customer_id"],
        state["category"],
        state["resolution"]
    )

    state["escalation_details"] = escalation_data

    print("\n=== ESCALATION AGENT ===")
    print(escalation_data)

    return state