# tools.py

from typing import Dict


def lookup_subscription(customer_id: str) -> Dict:
    """
    Mock billing database lookup.
    """

    if customer_id == "C-500":
        return {
            "plan": "Pro",
            "status": "Active",
            "duplicate_charge_detected": True,
            "last_payment": 29.99
        }

    return {
        "plan": "Basic",
        "status": "Active",
        "duplicate_charge_detected": False,
        "last_payment": 9.99
    }


def search_known_issues(query: str) -> Dict:
    """
    Mock technical issue database.
    """

    query = query.lower()

    if "crash" in query:
        return {
            "known_issue": True,
            "issue_id": "BUG-101",
            "workaround": "Clear app cache and reinstall."
        }

    return {
        "known_issue": False
    }


def feature_catalog_lookup(feature_name: str) -> Dict:
    """
    Mock feature roadmap lookup.
    """

    return {
        "exists": False,
        "planned": True,
        "release": "Q4 2026"
    }


def search_knowledge_base(question: str) -> Dict:
    """
    Mock FAQ search.
    """

    question = question.lower()

    if "export" in question:
        return {
            "found": True,
            "answer": (
                "Navigate to Settings > Reports "
                "and click Export."
            )
        }

    return {
        "found": False
    }


def lookup_account(customer_id: str) -> Dict:
    """
    Mock account lookup.
    """

    if customer_id == "C-999":
        return {
            "account_status": "Locked",
            "security_flag": True,
            "last_login": "Unknown"
        }

    return {
        "account_status": "Active",
        "security_flag": False,
        "last_login": "2026-06-20"
    }


def create_escalation_ticket(
    ticket_id: str,
    reason: str
) -> Dict:
    """
    Mock escalation system.
    """

    return {
        "escalation_id": f"ESC-{ticket_id}",
        "assigned_team": "Tier-2 Support",
        "status": "Open",
        "reason": reason
    }