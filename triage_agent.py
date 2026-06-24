from pydantic import BaseModel

from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


class TriageOutput(BaseModel):
    category: str


parser = JsonOutputParser(
    pydantic_object=TriageOutput
)


def triage_agent(state):

    prompt = f"""
You are a customer support triage agent.

Classify the ticket into exactly one category.

Available Categories:

- Billing
- Technical Issue
- Feature Request
- General Inquiry
- Account Management

{parser.get_format_instructions()}

Ticket:
{state["message"]}
"""

    response = llm.invoke(prompt)

    result = parser.parse(response.content)

    state["category"] = result["category"]

    print("\n=== TRIAGE ===")
    print(state["category"])

    return state