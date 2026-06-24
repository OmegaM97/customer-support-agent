def telegram_tool(
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
