from persistence import save_state, init_database, load_ticket


def save_to_db_agent(state):
    """Save the workflow state to the SQLite database."""
    save_state(state)
    
    ticket_id = state.get("ticket_id", "Unknown")
    print(f"Ticket {ticket_id} saved to SQLite database. /n {load_ticket(ticket_id)}")
    
    return state
