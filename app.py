import streamlit as st

# 1. Premium Clean Configuration
st.set_page_config(page_title="Smart AI Chatbot", page_icon="🤖", layout="centered")

# Custom UI Style for High Contrast
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
    /* Style form submit button for clean visibility */
    div.stFormSubmitButton > button {
        background-color: #38bdf8 !important;
        color: #0f172a !important;
        font-weight: bold !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🤖 Smart AI FAQ Chatbot</h1>", unsafe_allow_html=True)
st.write("---")

# Sidebar configurations
st.sidebar.title("🤖 Chatbot Capabilities")
st.sidebar.markdown("""
This AI chatbot handles universal queries:
- 📚 **Education & CS Fields**
- 👤 **Personal Chitchat**
- 🌍 **General Knowledge**
""")
st.sidebar.write("---")
st.sidebar.caption("Developer: Fatima\nID: CA/DF1/190219")

# 2. Comprehensive Multi-Category Knowledge Base
knowledge_base = {
    "cs": "After completing Computer Science, you can pursue specialized tracks like Artificial Intelligence, Data Science, Cyber Security, Cloud Computing, or full-stack software development. Master's degrees or professional certifications (AWS, Google AI) are also highly valuable.",
    "study": "After completing Computer Science, you can pursue specialized tracks like Artificial Intelligence, Data Science, Cyber Security, Cloud Computing, or full-stack software development. Master's degrees or professional certifications (AWS, Google AI) are also highly valuable.",
    "python": "You can learn Python by practicing fundamental concepts like loops, data structures, object-oriented programming, and working on micro-projects like web scrapers or automation scripts.",
    "ai": "Artificial Intelligence is the branch of computer science dedicated to simulating human intelligence processes through advanced neural networks and machine learning workflows.",
    "artificial": "Artificial Intelligence is the branch of computer science dedicated to simulating human intelligence processes through advanced neural networks and machine learning workflows.",
    "hi": "Hi Fatima! How can I assist you with your queries or educational tracks today?",
    "hello": "Hello Fatima! I hope you are having an amazing day. What would you like to explore today?",
    "hlo": "Hello Fatima! I hope you are having an amazing day. What would you like to explore today?",
    "how are you": "I am working perfectly and ready to answer your questions regarding computer science, education, or general knowledge!",
    "name": "I am an AI Smart Assistant configured by Fatima for her internship project.",
    "created": "I was developed by Fatima using Python and Streamlit web layout integration.",
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

# 4. Standard Form Input (Smart Check)
with st.form(key="chat_form", clear_on_submit=True):
    user_query = st.text_input(label="Ask me anything:", placeholder="Type here (e.g. study after cs)...", label_visibility="collapsed")
    submit_button = st.form_submit_button(label="Send Message")

if submit_button and user_query:
    st.markdown(f"<div class='chat-bubble-user'><b>👤 You:</b> {user_query}</div>", unsafe_allow_html=True)
    st.session_state.chat_history.append({"role": "user", "text": user_query})
    
    query_clean = user_query.strip().lower()
    
    chatbot_response = ""
    # Smart Word-by-Word Scanning
    for keyword, response in knowledge_base.items():
        if keyword in query_clean:
            chatbot_response = response
            break
            
    if not chatbot_response:
        chatbot_response = "❌ **Status: Unknown/Unsupported Question.** I am currently customized to answer multi-domain queries regarding Education (e.g., 'study after cs'), Personal chitchat, or General Knowledge. Please refine your phrase or ask about your career track!"

    st.markdown(f"<div class='chat-bubble-bot'><b>🤖 Bot:</b> {chatbot_response}</div>", unsafe_allow_html=True)
    st.session_state.chat_history.append({"role": "assistant", "text": chatbot_response})

st.write("---")
st.markdown("<p style='text-align: center; color: #64748b; font-size: 13px;'>Project Developed by Fatima | Student ID: CA/DF1/190219</p>", unsafe_allow_html=True)
