import streamlit as st
import requests
import plotly.express as px
import pandas as pd


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

st.markdown("### 🥧 Category Distribution")

try:
    counts = metrics["category_counts"]
    df_counts = pd.DataFrame({
        "Category": list(counts.keys()),
        "Count": list(counts.values())
    })

    fig_pie = px.pie(
        df_counts,
        names="Category",
        values="Count",
        color="Category",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_pie, use_container_width=True)

except Exception as e:
    st.error(f"Failed to load pie chart: {e}")

st.markdown("### 📦 Emissions by Category (kg CO₂e)")

try:
    timeline = metrics["timestamps"]

    df_em = pd.DataFrame([{
        "Category": entry["intent"],
        "Emission": entry["emission"]
    } for entry in timeline if entry["emission"] is not None])

    if not df_em.empty:
        fig_bar = px.bar(
            df_em.groupby("Category").sum().reset_index(),
            x="Category",
            y="Emission",
            color="Category",
            text="Emission",
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No emission data available yet.")

except Exception as e:
    st.error(f"Bar chart failed: {e}")

st.markdown("### ⏳ Emission Timeline")

try:
    df_time = pd.DataFrame([
        {
            "Timestamp": entry["ts"],
            "Emission": entry["emission"]
        }
        for entry in timeline if entry["emission"] is not None
    ])

    if not df_time.empty:
        df_time["Timestamp"] = pd.to_datetime(df_time["Timestamp"])

        fig_line = px.line(
            df_time,
            x="Timestamp",
            y="Emission",
            markers=True,
            color_discrete_sequence=["#2E7D32"]  # eco green
        )
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("No timestamped emission entries yet.")

except Exception as e:
    st.error(f"Line chart failed: {e}")

st.markdown("### 🌟 Key Indicators")

colA, colB, colC = st.columns(3)

colA.metric("🌍 Total CO₂ Logged", f"{metrics['total_emissions_logged']} kg")
colB.metric("📌 Queries Made", metrics["total_queries"])
colC.metric("👥 Active Sessions", len(metrics["session_query_counts"]))

