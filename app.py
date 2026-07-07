import streamlit as st

# 1. Premium Page Setup
st.set_page_config(page_title="Universal AI Chatbot", page_icon="🤖", layout="centered")

# Custom Professional UI Style with High Visibility Text
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
    }
    .sub-title {
        color: #94a3b8;
        text-align: center;
        font-size: 14px;
        margin-bottom: 30px;
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
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🤖 Multi-Category Smart AI Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>CodeAlpha Artificial Intelligence Internship - Task 2</p>", unsafe_allow_html=True)
st.write("---")

# Sidebar helper to show available domains
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
    # --- EDUCATION & CS ---
    "study after cs": "After completing Computer Science, you can pursue specialized tracks like Artificial Intelligence, Data Science, Cyber Security, Cloud Computing, or full-stack software development. Master's degrees or professional certifications (AWS, Google AI) are also highly valuable.",
    "what is computer science": "Computer Science is the study of computers and computational systems, focusing on software algorithms, architecture, and advanced data processing.",
    "how to learn python": "You can learn Python by practicing fundamental concepts like loops, data structures, object-oriented programming, and working on micro-projects like web scrapers or automation scripts.",
    "what is artificial intelligence": "Artificial Intelligence is the branch of computer science dedicated to simulating human intelligence processes through advanced neural networks and machine learning workflows.",
    
    # --- GREETINGS & PERSONAL ---
    "hi": "Hi Fatima! How can I assist you with your queries or educational tracks today?",
    "hello": "Hello Fatima! I hope you are having an amazing day. What would you like to explore today?",
    "how are you": "I am working perfectly and ready to answer your questions regarding computer science, education, or general knowledge!",
    "what is your name": "I am an AI Smart Assistant configured by Fatima for her CodeAlpha internship project.",
    "who created you": "I was developed by Fatima using Python and Streamlit web layout integration.",
    
    # --- GENERAL KNOWLEDGE ---
    "capital of pakistan": "The capital city of Pakistan is Islamabad.",
    "largest ocean": "The Pacific Ocean is the largest and deepest body of water on Earth.",
    "days in a year": "A standard year contains 365 days, while a leap year contains 366 days."
}

# 3. Dialogue Memory Management
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display entire dialogue history with new distinct high-visibility layouts
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-bubble-user'><b>👤 You:</b> {msg['text']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-bot'><b>🤖 Bot:</b> {msg['text']}</div>", unsafe_allow_html=True)

# 4. User Input Prompt Bar
user_query = st.chat_input("Ask me anything...")

if user_query:
    # Render user query instantly
    st.markdown(f"<div class='chat-bubble-user'><b>👤 You:</b> {user_query}</div>", unsafe_allow_html=True)
    st.session_state.chat_history.append({"role": "user", "text": user_query})
    
    # Clean string processing for checking database
    query_clean = user_query.strip().lower()
    
    # Matching logic looking for keywords (e.g., 'study after cs')
    chatbot_response = ""
    for keyword, response in knowledge_base.items():
        if keyword in query_clean:
            chatbot_response = response
            break
            
    # Default fallback behavior for unknown inputs
    if not chatbot_response:
        chatbot_response = "❌ **Status: Unknown/Unsupported Question.** I am currently customized to answer multi-domain queries regarding Education (e.g., 'study after cs'), Personal chitchat, or General Knowledge. Please refine your phrase or ask about your career track!"

    # Render bot response cleanly
    st.markdown(f"<div class='chat-bubble-bot'><b>🤖 Bot:</b> {chatbot_response}</div>", unsafe_allow_html=True)
    st.session_state.chat_history.append({"role": "assistant", "text": chatbot_response})

st.write("---")
st.caption("Developed by Fatima | Student ID: CA/DF1/190219 | CodeAlpha Internship Assignment")
