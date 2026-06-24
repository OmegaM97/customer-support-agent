def human_approval_agent(state):

    print("\n=== HUMAN APPROVAL ===")

    print(f"""
Ticket ID:
{state["ticket_id"]}

Category:
{state["category"]}

Resolution:
{state["resolution"]}

Confidence:
{state["confidence"]}
""")

    answer = input(
        "Approve escalation? (y/n): "
    ).strip().lower()

    state["human_approved"] = (
        answer == "y"
    )

    return state