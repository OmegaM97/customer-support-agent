import os
import requests

from dotenv import load_dotenv

load_dotenv()


def telegram_tool(
    ticket_id,
    customer_id,
    category,
    resolution
):
    """
    Sends escalation details
    to Telegram support group.
    """

    token = os.getenv(
        "TELEGRAM_BOT_TOKEN"
    )

    chat_id = os.getenv(
        "TELEGRAM_CHAT_ID"
    )

    message = f"""
🚨 SUPPORT ESCALATION

Ticket ID: {ticket_id}

Customer ID: {customer_id}

Category: {category}

Resolution Attempt:
{resolution}

Status: OPEN

Assigned Team:
Tier 2 Support
"""

    response = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": message
        }
    )

    if response.status_code == 200:

        return {
            "status": "sent",
            "assigned_team": "Tier 2 Support"
        }

    return {
        "status": "failed",
        "error": response.text
    }