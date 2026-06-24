import sqlite3
import json
import os

DB_PATH = "db/support.db"


def init_database():
    """Initialize SQLite database and create tables if they don't exist."""
    os.makedirs("db", exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id TEXT PRIMARY KEY,
            customer_id TEXT,
            message TEXT,
            category TEXT,
            tool_result TEXT,
            resolution TEXT,
            confidence REAL,
            escalation_required INTEGER,
            escalation_details TEXT,
            final_response TEXT
        )
    """)
    
    conn.commit()
    conn.close()


def save_state(state):
    """Save the workflow state to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Convert dict fields to JSON strings
    tool_result = json.dumps(state.get("tool_result", {}))
    escalation_details = json.dumps(state.get("escalation_details", {}))
    
    cursor.execute("""
        INSERT OR REPLACE INTO tickets (
            ticket_id,
            customer_id,
            message,
            category,
            tool_result,
            resolution,
            confidence,
            escalation_required,
            escalation_details,
            final_response
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        state.get("ticket_id"),
        state.get("customer_id"),
        state.get("message"),
        state.get("category"),
        tool_result,
        state.get("resolution"),
        state.get("confidence"),
        int(state.get("escalation_required", False)),
        escalation_details,
        state.get("final_response")
    ))
    
    conn.commit()
    conn.close()


def load_ticket(ticket_id):
    """Load a saved ticket from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM tickets WHERE ticket_id = ?
    """, (ticket_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
    
    # Convert JSON strings back to dicts
    tool_result = json.loads(row[4])
    escalation_details = json.loads(row[8])
    
    ticket = {
        "ticket_id": row[0],
        "customer_id": row[1],
        "message": row[2],
        "category": row[3],
        "tool_result": tool_result,
        "resolution": row[5],
        "confidence": row[6],
        "escalation_required": bool(row[7]),
        "escalation_details": escalation_details,
        "final_response": row[9]
    }
    
    return ticket
