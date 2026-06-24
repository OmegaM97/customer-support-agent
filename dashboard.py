import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "db/support.db"

st.set_page_config(
    page_title="Customer Support Analytics",
    page_icon="📊",
    layout="wide"
)


@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        "SELECT * FROM tickets",
        conn
    )

    conn.close()

    return df


df = load_data()

st.title("📊 Customer Support Escalation Dashboard")

if df.empty:
    st.warning("No ticket data found.")
    st.stop()


total_tickets = len(df)

escalated_tickets = df["escalation_required"].sum()

escalation_rate = (
    escalated_tickets / total_tickets * 100
)

resolved_tickets = (
    df["resolution"]
    .fillna("")
    .str.strip()
    .ne("")
    .sum()
)

resolution_rate = (
    resolved_tickets / total_tickets * 100
)

avg_confidence = df["confidence"].mean()


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Tickets",
    total_tickets
)

col2.metric(
    "Escalation Rate",
    f"{escalation_rate:.1f}%"
)

col3.metric(
    "Resolution Rate",
    f"{resolution_rate:.1f}%"
)

col4.metric(
    "Avg Confidence",
    f"{avg_confidence:.2f}"
)

st.divider()


st.subheader("Ticket Categories")

category_counts = (
    df["category"]
    .value_counts()
    .reset_index()
)

category_counts.columns = [
    "Category",
    "Tickets"
]

st.bar_chart(
    category_counts.set_index("Category")
)

st.subheader("Escalation Breakdown")

escalation_data = pd.DataFrame({
    "Status": ["Escalated", "Not Escalated"],
    "Count": [
        escalated_tickets,
        total_tickets - escalated_tickets
    ]
})

st.dataframe(
    escalation_data,
    use_container_width=True
)

st.subheader("Average Confidence by Category")

confidence_by_category = (
    df.groupby("category")["confidence"]
    .mean()
    .sort_values(ascending=False)
)

st.bar_chart(confidence_by_category)


st.subheader("Recent Tickets")

st.dataframe(
    df[
        [
            "ticket_id",
            "customer_id",
            "category",
            "confidence",
            "escalation_required"
        ]
    ],
    use_container_width=True
)