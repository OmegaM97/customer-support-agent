from langchain_groq import ChatGroq
from tools.telegram_tool import telegram_tool


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

def escalation_agent(state):

    escalation_data = telegram_tool(
        state["ticket_id"],
        state["resolution"]
    )

    state["escalation_details"] = escalation_data

    print("\n=== ESCALATION AGENT ===")
    print(escalation_data)

    return state