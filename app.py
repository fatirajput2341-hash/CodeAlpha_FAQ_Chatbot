import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Page Configuration Setup
st.set_page_config(page_title="Universal AI Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 Multi-Category Smart AI Chatbot")
st.markdown("CodeAlpha Artificial Intelligence Internship - Task 2 Enhanced")
st.write("---")

# 2. Multi-Category Universal FAQs Database (Education, Personal, General)
faq_database = {
    # --- EDUCATION CATEGORY ---
    "what is computer science": "Computer Science is the study of computers and computational systems, focusing on software, algorithms, and data processing.",
    "how to learn python programming": "You can learn Python by practicing basic syntax, loops, functions, and building small projects like calculators or automation scripts.",
    "what is artificial intelligence": "Artificial Intelligence (AI) is the simulation of human intelligence processes by machines, especially computer systems.",
    "why is education important": "Education empowers minds, provides critical thinking skills, and opens up professional career opportunities globally.",
    
    # --- PERSONAL / CHIT-CHAT CATEGORY ---
    "hello": "Hello Fatima! I hope you are having a wonderful day. How can I help you today?",
    "hi": "Hi there! How can I assist you with your queries today?",
    "how are you": "I am doing great, thank you for asking! I am ready to answer your education and personal questions.",
    "what is your name": "I am your personal AI Assistant developed by Fatima for the CodeAlpha internship.",
    "who created you": "I was created and customized by Fatima as part of her AI Internship project.",
    
    # --- GENERAL KNOWLEDGE CATEGORY ---
    "what is the capital of pakistan": "The capital city of Pakistan is Islamabad.",
    "which is the largest ocean on earth": "The Pacific Ocean is the largest and deepest ocean on Earth.",
    "how many days are there in a year": "There are 365 days in a standard year, and 366 days in a leap year."
}

faq_questions = list(faq_database.keys())

# Sidebar helper to show available domains
st.sidebar.title("🤖 Chatbot Capabilities")
st.sidebar.markdown("""
This AI chatbot can intelligently handle queries across multiple categories:
- 📚 **Education & Tech**
- 👤 **Personal & Greetings**
- 🌍 **General Knowledge**
""")
st.sidebar.write("---")
st.sidebar.caption("Developer: Fatima\nID: CA/DF1/190219")

# 3. Chat Interface Layout
st.markdown("### 💬 Ask me anything (Education, Personal, GK):")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["text"])

user_query = st.chat_input("Ask a question...")

if user_query:
    with st.chat_message("user"):
        st.write(user_query)
    st.session_state.messages.append({"role": "user", "text": user_query})
    
    # 4. Processing Intent via Cosine Similarity
    all_texts = faq_questions + [user_query]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    best_match_idx = similarity_scores.argmax()
    highest_score = similarity_scores[best_match_idx]
    
    # 5. Response logic with Right/Wrong Check
    with st.chat_message("assistant"):
        if highest_score > 0.35: # Intent match threshold
            matched_question = faq_questions[best_match_idx]
            chatbot_response = faq_database[matched_question]
            st.write(chatbot_response)
        else:
            # Handling wrong/unsupported questions clearly
            chatbot_response = "❌ **Status: Unknown/Wrong Query.** I am sorry, this question does not match my current database (Education, Personal, GK). Please ask something relevant or check your spelling!"
            st.write(chatbot_response)
            
    st.session_state.messages.append({"role": "assistant", "text": chatbot_response})

st.write("---")
st.caption("Developed by Fatima | Student ID: CA/DF1/190219 | CodeAlpha Internship Assignment")
