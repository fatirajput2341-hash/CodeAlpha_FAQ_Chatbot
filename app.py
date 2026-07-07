import streamlit as st
import requests

# 1. Premium Clean Configuration
st.set_page_config(page_title="Universal AI Chatbot", page_icon="🤖", layout="centered")

# Custom UI Style for Premium High-Visibility Look
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #0f172a, #1e293b);
        color: #f8fafc;
    }
    .main-title {
        color: #38bdf8;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: center;
        font-weight: 800;
        margin-top: -20px;
    }
    .chat-bubble-user {
        background-color: #334155;
        color: #ffffff;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 10px;
        border-left: 4px solid #38bdf8;
    }
    .chat-bubble-bot {
        background-color: #1e293b;
        color: #f1f5f9;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 10px;
        border-left: 4px solid #34d399;
    }
    div.stFormSubmitButton > button {
        background-color: #38bdf8 !important;
        color: #0f172a !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🤖 Smart AI FAQ Chatbot</h1>", unsafe_allow_html=True)
st.write("---")

# Sidebar configurations
st.sidebar.title("🤖 Chatbot Capabilities")
st.sidebar.markdown("""
This AI chatbot is fully dynamic and handles all types of queries:
- 📚 **Education & Task Help**
- 👤 **Personal Decisions & Chitchat**
- 🌍 **General Knowledge**
""")
st.sidebar.write("---")
st.sidebar.caption("Developer: Fatima\nID: CA/DF1/190219")

# 2. Dialogue Memory Management
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-bubble-user'><b>👤 You:</b> {msg['text']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-bot'><b>🤖 Bot:</b> {msg['text']}</div>", unsafe_allow_html=True)

# 3. Standard Form Input Box
with st.form(key="chat_form", clear_on_submit=True):
    user_query = st.text_input(label="Ask me anything:", placeholder="Ask anything (Education, Personal, Tasks)...", label_visibility="collapsed")
    submit_button = st.form_submit_button(label="Send Message")

if submit_button and user_query:
    st.markdown(f"<div class='chat-bubble-user'><b>👤 You:</b> {user_query}</div>", unsafe_allow_html=True)
    st.session_state.chat_history.append({"role": "user", "text": user_query})
    
    # 4. Connecting with DuckDuckGo AI Free Endpoint API (No API Key Required, Dynamic AI)
    chatbot_response = ""
    try:
        with st.spinner("Thinking..."):
            # Clean system instructions to maintain custom human look verification
            system_prompt = "You are a helpful, smart AI assistant built by Fatima for her CodeAlpha internship. Answer all user questions comprehensively in simple text format like a pro human writer."
            
            # Direct API request to live duckduckgo secure endpoint architecture
            api_url = "https://pollinations.ai"
            payload = {"messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_query}]}
            
            response = requests.post(api_url, json=payload, timeout=15)
            if response.status_code == 200:
                chatbot_response = response.text
            else:
                chatbot_response = "🤖 Connection is slightly busy, but I am here! Could you please try asking your question again?"
    except Exception:
        chatbot_response = "🤖 System is refreshing its pipelines. Please re-send your message to fetch response!"

    # Render bot response cleanly
    st.markdown(f"<div class='chat-bubble-bot'><b>🤖 Bot:</b> {chatbot_response}</div>", unsafe_allow_html=True)
    st.session_state.chat_history.append({"role": "assistant", "text": chatbot_response})

st.write("---")
st.markdown("<p style='text-align: center; color: #64748b; font-size: 13px;'>Project Developed by Fatima | Student ID: CA/DF1/190219</p>", unsafe_allow_html=True)
