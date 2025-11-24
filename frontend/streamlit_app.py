import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="EcoMentor",
    layout="wide",
    page_icon="🌱"
)

st.title("🌱 EcoMentor — Your Sustainability Coach")
st.subheader("💬 Chat with EcoMentor")

# ---------------------------
# SIDEBAR
# ---------------------------
session_id = st.sidebar.text_input("Session ID", value="ujwal123")

# ---------------------------
# CHAT HISTORY
# ---------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------------------
# CHAT CSS
# ---------------------------
st.markdown("""
<style>
.user-msg {
    background-color: #DCFCE7;
    padding: 8px 12px;
    border-radius: 12px;
    margin: 8px 0;
    width: fit-content;
    max-width: 80%;
}
.bot-msg {
    background-color: #E5E7EB;
    padding: 8px 12px;
    border-radius: 12px;
    margin: 8px 0;
    width: fit-content;
    max-width: 80%;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# CHAT DISPLAY WITHOUT CONTAINER BOX
# ---------------------------
for sender, msg in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f'<div class="user-msg"><b>You:</b> {msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-msg"><b>EcoMentor:</b> {msg}</div>', unsafe_allow_html=True)

# ---------------------------
# USER INPUT
# ---------------------------
user_input = st.text_input("Type your message...")

if st.button("Send"):
    if user_input.strip():
        st.session_state.chat_history.append(("You", user_input))

        try:
            response = requests.post(
                f"{API_BASE}/chat",
                json={"message": user_input, "session_id": session_id},
                timeout=10
            )
            data = response.json()
            reply = data.get("response", "No reply")
        except Exception as e:
            reply = f"Error: {str(e)}"

        st.session_state.chat_history.append(("EcoMentor", reply))
        st.rerun()

# ---------------------------
# DASHBOARD SECTIONS BELOW
# ---------------------------
st.markdown("---")
st.subheader("📊 Weekly Impact Summary")

try:
    summary = requests.get(f"{API_BASE}/weekly_summary", params={"session_id": session_id}).json()
    weekly = summary["weekly_summary"]

    col1, col2 = st.columns(2)
    col1.metric("Weekly CO₂e", f"{weekly['weekly_total_kg']} kg")
    col2.write("Breakdown:")
    col2.json(weekly["breakdown"])

except:
    st.warning("Error loading weekly summary.")

st.markdown("---")
st.subheader("📈 System Metrics Overview")

try:
    metrics = requests.get(f"{API_BASE}/metrics").json()["metrics"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Queries", metrics["total_queries"])
    col2.metric("Total Emissions Logged", f"{metrics['total_emissions_logged']} kg")
    col3.metric("Active Sessions", len(metrics["session_query_counts"]))

    st.write("Category Counts:")
    st.bar_chart(metrics["category_counts"])

except:
    st.warning("Error loading metrics.")
