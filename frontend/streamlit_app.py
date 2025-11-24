import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="EcoMentor",
    layout="wide",
    page_icon="🌱"
)

# --- Sidebar ---
st.sidebar.header("EcoMentor Settings")
session_id = st.sidebar.text_input("Session ID", value="ujwal123")
st.sidebar.write("Your personalized sustainability session.")

st.title("🌱 EcoMentor — Your Sustainability Coach")


# ----------------------------------------------------
# 🌱 ECO-MENTOR CHAT WIDGET (COMPACT + SCROLLABLE)
# ----------------------------------------------------
st.subheader("💬 Chat with EcoMentor")

# CSS for chat styling
st.markdown("""
<style>
.chat-window {
    background-color: #f7f7f7;
    border-radius: 12px;
    height: 330px;
    padding: 10px;
    overflow-y: auto;
    border: 1px solid #D0D0D0;
}

.user-msg {
    background-color: #DCFCE7; /* Light green */
    padding: 8px 12px;
    border-radius: 12px;
    margin-bottom: 8px;
    width: fit-content;
    max-width: 80%;
}

.bot-msg {
    background-color: #E5E7EB; /* Light grey */
    padding: 8px 12px;
    border-radius: 12px;
    margin-bottom: 8px;
    width: fit-content;
    max-width: 80%;
}
</style>
""", unsafe_allow_html=True)

# Session state to store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat display container
chat_container = st.container()
with chat_container:
    st.markdown('<div class="chat-window">', unsafe_allow_html=True)

    # Render stored chat history
    for sender, msg in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f'<div class="user-msg"><b>You:</b> {msg}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-msg"><b>EcoMentor:</b> {msg}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Message input
user_input = st.text_input("Type your message...")

if st.button("Send"):
    if user_input.strip():
        # Save user message
        st.session_state.chat_history.append(("You", user_input))

        # Call backend
        try:
            response = requests.post(
                f"{API_BASE}/chat",
                json={"message": user_input, "session_id": session_id},
                timeout=10
            )
            data = response.json()
            reply = data.get("response", "Error: No response from EcoMentor")

            # Save bot reply
            st.session_state.chat_history.append(("EcoMentor", reply))

        except Exception as e:
            st.session_state.chat_history.append(("EcoMentor", f"Error: {str(e)}"))

        st.experimental_rerun()



# --- Weekly Summary ---
st.subheader("📊 Weekly Impact Summary")

try:
    summary = requests.get(f"{API_BASE}/weekly_summary", params={"session_id": session_id}).json()
    weekly = summary["weekly_summary"]

    st.metric("Weekly CO₂e", f"{weekly['weekly_total_kg']} kg CO₂e")
    st.write("Category Breakdown:", weekly["breakdown"])
except:
    st.warning("Weekly summary unavailable.")


# --- Metrics Dashboard ---
st.subheader("📈 System Metrics Overview")

try:
    metrics = requests.get(f"{API_BASE}/metrics").json()["metrics"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Queries", metrics["total_queries"])
    col2.metric("Total Emissions Logged", f"{metrics['total_emissions_logged']} kg")
    col3.metric("Active Sessions", len(metrics["session_query_counts"]))

    st.write("### Category Counts")
    st.bar_chart(metrics["category_counts"])

except:
    st.warning("Metrics unavailable.")
