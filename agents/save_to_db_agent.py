from persistence import save_state, init_database, load_ticket


def save_to_db_agent(state):
    """Save the workflow state to the SQLite database."""
    save_state(state)
    
    return state
