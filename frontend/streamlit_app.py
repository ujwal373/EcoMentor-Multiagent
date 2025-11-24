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
# SESSION ID
# ---------------------------
session_id = st.sidebar.text_input("Session ID", value="ujwal123")

# ---------------------------
# Ensure chat history exists
# ---------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------------------
# CHAT WINDOW STYLE
# ---------------------------
chat_css = """
<style>
.chat-window {
    background-color: #f7f7f7;
    border-radius: 12px;
    height: 330px;
    padding: 10px;
    overflow-y: auto;
    border: 1px solid #D0D0D0;
}

/* User bubble */
.user-msg {
    background-color: #DCFCE7;
    padding: 8px 12px;
    border-radius: 12px;
    margin-bottom: 8px;
    width: fit-content;
    max-width: 80%;
}

/* Bot bubble */
.bot-msg {
    background-color: #E5E7EB;
    padding: 8px 12px;
    border-radius: 12px;
    margin-bottom: 8px;
    width: fit-content;
    max-width: 80%;
}
</style>
"""

st.markdown(chat_css, unsafe_allow_html=True)

# ---------------------------
# CHAT DISPLAY BOX
# ---------------------------
chat_box = st.container()

with chat_box:
    st.markdown('<div class="chat-window" id="chatbox">', unsafe_allow_html=True)

    # Render chat history INSIDE chat window
    for sender, msg in st.session_state.chat_history:
        if sender == "You":
            st.markdown(
                f'<div class="user-msg"><b>You:</b> {msg}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="bot-msg"><b>EcoMentor:</b> {msg}</div>',
                unsafe_allow_html=True
            )

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# USER INPUT
# ---------------------------
user_input = st.text_input("Type your message...")

if st.button("Send"):
    if user_input.strip():

        # → Save user message
        st.session_state.chat_history.append(("You", user_input))

        # → Call backend
        try:
            response = requests.post(
                f"{API_BASE}/chat",
                json={"message": user_input, "session_id": session_id},
                timeout=10
            )
            data = response.json()
            reply = data.get("response", "(No reply from backend)")
        except Exception as e:
            reply = f"Error: {str(e)}"

        # → Save bot reply
        st.session_state.chat_history.append(("EcoMentor", reply))

        st.rerun()
