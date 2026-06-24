# tools.py

from typing import Dict


def lookup_subscription(customer_id: str) -> Dict:
    """
    Subscription information.
    """

    if customer_id == "C-500":
        return {
            "plan": "Pro",
            "status": "Active",
            "renewal_date": "2026-07-01"
        }

    return {
        "plan": "Basic",
        "status": "Active",
        "renewal_date": "2026-07-01"
    }


def lookup_payment_history(customer_id: str) -> Dict:
    """
    Payment transaction history.
    """

    if customer_id == "C-500":
        return {
            "payments": [
                {
                    "date": "2026-06-20",
                    "amount": 29.99
                },
                {
                    "date": "2026-06-20",
                    "amount": 29.99
                }
            ],
            "duplicate_charge_detected": True
        }

    return {
        "payments": [
            {
                "date": "2026-06-20",
                "amount": 9.99
            }
        ],
        "duplicate_charge_detected": False
    }


def lookup_refund_status(customer_id: str) -> Dict:
    """
    Refund lookup.
    """

    if customer_id == "C-700":
        return {
            "refund_requested": True,
            "refund_status": "Processing",
            "estimated_completion": "3 business days"
        }

    return {
        "refund_requested": False
    }


def search_known_issues(query: str) -> Dict:
    """
    Known bug database.
    """

    query = query.lower()

    if "crash" in query:
        return {
            "known_issue": True,
            "issue_id": "BUG-101",
            "workaround": "Clear cache and reinstall."
        }

    return {
        "known_issue": False
    }


def lookup_system_status(_: str) -> Dict:
    """
    Mock system health dashboard.
    """

    return {
        "api_status": "Operational",
        "mobile_app_status": "Operational",
        "database_status": "Operational"
    }


def feature_catalog_lookup(feature_name: str) -> Dict:
    """
    Existing feature lookup.
    """

    return {
        "exists": False,
        "planned": True,
        "release": "Q4 2026"
    }


def roadmap_lookup(feature_name: str) -> Dict:
    """
    Product roadmap lookup.
    """

    return {
        "roadmap_item": True,
        "priority": "Medium",
        "target_release": "Q4 2026"
    }


def search_knowledge_base(question: str) -> Dict:
    """
    Internal KB search.
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


def faq_lookup(question: str) -> Dict:
    """
    FAQ lookup.
    """

    question = question.lower()

    if "password" in question:
        return {
            "found": True,
            "answer": (
                "Use the Forgot Password option "
                "on the login screen."
            )
        }

    return {
        "found": False
    }


def lookup_account(customer_id: str) -> Dict:
    """
    Account information.
    """

    if customer_id == "C-999":
        return {
            "account_status": "Locked",
            "security_flag": True
        }

    return {
        "account_status": "Active",
        "security_flag": False
    }


def lookup_login_history(customer_id: str) -> Dict:
    """
    Login activity.
    """

    if customer_id == "C-999":
        return {
            "last_login": "Unknown",
            "suspicious_activity": True,
            "failed_login_attempts": 12
        }

    return {
        "last_login": "2026-06-20",
        "suspicious_activity": False,
        "failed_login_attempts": 0
    }

def create_escalation_ticket(
    ticket_id: str,
    reason: str
) -> Dict:
    """
    Mock escalation ticket creation.
    """

    return {
        "escalation_id": f"ESC-{ticket_id}",
        "assigned_team": "Tier-2 Support",
        "status": "Open",
        "reason": reason
    }