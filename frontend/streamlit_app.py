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


# --- Chat Section ---
st.subheader("Chat with EcoMentor")

user_input = st.text_input("Ask something about your carbon footprint...")
chat_button = st.button("Send")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if chat_button and user_input:
    try:
        response = requests.post(
            f"{API_BASE}/chat",
            json={"message": user_input, "session_id": session_id},
            timeout=10
        )
        data = response.json()
        reply = data["response"]

        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("EcoMentor", reply))

    except Exception as e:
        st.error("Error connecting to backend.")
        st.error(str(e))


# Display chat history
for sender, msg in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**🧑 You:** {msg}")
    else:
        st.markdown(f"**🤖 EcoMentor:** {msg}")


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
