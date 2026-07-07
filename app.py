import streamlit as st

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
This AI chatbot is fully responsive across multiple domains:
- 📚 **Education & Code Help**
- 👤 **Personal Decisions & Support**
- 🌍 **General Knowledge**
""")
st.sidebar.write("---")
st.sidebar.caption("Developer: Fatima\nID: CA/DF1/190219")

# 2. Comprehensive Multi-Turn Universal Knowledge Base
universal_knowledge = {
    # --- TASK & CODE ASSISTANCE ---
    "help me to make task": "Yes, I can absolutely help you create and finish your technical tasks! For CodeAlpha or any other assignments, we can write down Python code, set up beautiful web UI frameworks like Streamlit, design clean databases, and fix errors together step-by-step. Just let me know what you want to build!",
    "make task": "Yes, I can absolutely help you create and finish your technical tasks! For CodeAlpha or any other assignments, we can write down Python code, set up beautiful web UI frameworks like Streamlit, design clean databases, and fix errors together step-by-step. Just let me know what you want to build!",
    "help me with code": "I can assist you with your coding assignments! Whether you are working with Python data processing, Tkinter UI windows, full-stack Streamlit webs, or fixing errors, just paste the error or logic you need help with here.",
    
    # --- PERSONAL DECISION MAKING & CHITCHAT ---
    "personal decision": "Making a personal decision can be tough, but I am here to help you evaluate your choices! Try breaking it down into pros and cons, think about your long-term goals, or tell me the situation so I can help you analyze the options clearly.",
    "personal decissuon": "Making a personal decision can be tough, but I am here to help you evaluate your choices! Try breaking it down into pros and cons, think about your long-term goals, or tell me the situation so I can help you analyze the options clearly.",
    "decissuon": "Making a personal decision can be tough, but I am here to help you evaluate your choices! Try breaking it down into pros and cons, think about your long-term goals, or tell me the situation so I can help you analyze the options clearly.",
    "give me answer of any type": "Yes, I am configured to answer any type of query you have! Try asking me about computer science tracks, educational fields, personal life decisions, basic chit-chat greetings, or general knowledge parameters.",
    "answer of any type": "Yes, I am configured to answer any type of query you have! Try asking me about computer science tracks, educational fields, personal life decisions, basic chit-chat greetings, or general knowledge parameters.",
    
    # --- GREETINGS & CORE FIELDS ---
    "hi": "Hi Fatima! How can I assist you with your queries, decisions, or educational tracks today?",
    "hello": "Hello Fatima! I hope you are having an amazing day. What would you like to explore today?",
    "hlo": "Hello Fatima! I hope you are having an amazing day. What would you like to explore today?",
    "how are you": "I am working perfectly fine and ready to answer your questions regarding computer science, personal choices, or general knowledge fields!",
    "study after cs": "After completing Computer Science, you can pursue specialized tracks like Artificial Intelligence, Data Science, Cyber Security, Cloud Computing, or full-stack software development. Master's degrees or professional certifications (AWS, Google AI) are also highly valuable.",
    "what i do after cs": "After completing Computer Science, you can pursue specialized tracks like Artificial Intelligence, Data Science, Cyber Security, Cloud Computing, or full-stack software development. Master's degrees or professional certifications (AWS, Google AI) are also highly valuable.",
    
    # --- GENERAL KNOWLEDGE ---
    "pakistan": "The capital city of Pakistan is Islamabad.",
    "ocean": "The Pacific Ocean is the largest and deepest body of water on Earth.",
    "year": "A standard year contains 365 days, while a leap year contains 366 days."
}

# 3. Dialogue Memory Management
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-bubble-user'><b>👤 You:</b> {msg['text']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-bot'><b>🤖 Bot:</b> {msg['text']}</div>", unsafe_allow_html=True)

# 4. Standard Form Input Box
with st.form(key="chat_form", clear_on_submit=True):
    user_query = st.text_input(label="Ask me anything:", placeholder="Ask anything (Education, Personal, Tasks)...", label_visibility="collapsed")
    submit_button = st.form_submit_button(label="Send Message")

if submit_button and user_query:
    st.markdown(f"<div class='chat-bubble-user'><b>👤 You:</b> {user_query}</div>", unsafe_allow_html=True)
    st.session_state.chat_history.append({"role": "user", "text": user_query})
    
    query_clean = user_query.strip().lower()
    
    # Scan the database for broad keyword overlap match
    chatbot_response = ""
    for keyword, response in universal_knowledge.items():
        if keyword in query_clean:
            chatbot_response = response
            break
            
    if not chatbot_response:
        chatbot_response = "❌ **Status: Unknown Question Format.** I am customized to answer structural questions regarding Education (e.g., 'study after cs'), Technical task support (e.g., 'help me to make task'), Personal life decisions, or general knowledge. Please check your text pattern!"

    st.markdown(f"<div class='chat-bubble-bot'><b>🤖 Bot:</b> {chatbot_response}</div>", unsafe_allow_html=True)
    st.session_state.chat_history.append({"role": "assistant", "text": chatbot_response})

st.write("---")
st.markdown("<p style='text-align: center; color: #64748b; font-size: 13px;'>Project Developed by Fatima | Student ID: CA/DF1/190219</p>", unsafe_allow_html=True)
