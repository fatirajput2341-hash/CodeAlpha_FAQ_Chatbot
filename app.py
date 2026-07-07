import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Page Configuration Setup
st.set_page_config(page_title="FAQ Chatbot", page_icon="💬", layout="centered")

st.title("💬 AI Chatbot for FAQs")
st.markdown("CodeAlpha Artificial Intelligence Internship Task 2")
st.write("---")

# 2. Collect FAQs Dataset (Topic: CodeAlpha Internship FAQs)
faq_data = {
    "What is CodeAlpha?": "CodeAlpha is a software development company that provides virtual internship programs for students to gain real-world experience.",
    "How can I submit my internship tasks?": "You can submit your assigned tasks using the official submission form link provided in your email or official WhatsApp group.",
    "What is the duration of the internship?": "The internship duration is typically one month, as mentioned in your offer letter.",
    "Will I get a certificate after completion?": "Yes, you will receive a QR-verified completion certificate and a letter of recommendation based on your performance.",
    "Is it mandatory to complete all 4 tasks?": "No, you are required to complete only 2 or 3 mandatory tasks mentioned in your task document.",
    "Where should I upload my technical projects?": "You must upload all your technical project source code to a public GitHub repository.",
    "How can I contact the support team?": "You can reach out to the support team by emailing support@codealpha.tech or calling +91 95550 54118."
}

faq_questions = list(faq_data.keys())

# 3. Simple Chat UI Logic
st.markdown("### Ask Anything About CodeAlpha Internship:")

# Session state to maintain chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["text"])

# User input text field
user_query = st.chat_input("Type your question here...")

if user_query:
    # Display user message
    with st.chat_message("user"):
        st.write(user_query)
    st.session_state.messages.append({"role": "user", "text": user_query})
    
    # 4. Preprocessing and Matching using Cosine Similarity
    # Vectorizing the questions and user query to match intent
    all_texts = faq_questions + [user_query]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    # Calculate similarity scores between user query and all FAQ questions
    similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])[0]
    best_match_idx = similarity_scores.argmax()
    highest_score = similarity_scores[best_match_idx]
    
    # 5. Display the best matching answer as a chatbot response
    with st.chat_message("assistant"):
        if highest_score > 0.3:  # Threshold for accurate matching
            matched_question = faq_questions[best_match_idx]
            chatbot_response = faq_data[matched_question]
            st.write(chatbot_response)
        else:
            chatbot_response = "I am sorry, I couldn't find an accurate answer to that. Please email support@codealpha.tech for more help!"
            st.write(chatbot_response)
            
    st.session_state.messages.append({"role": "assistant", "text": chatbot_response})

st.write("---")
st.caption("Developed by Fatima | Student ID: CA/DF1/190219 | CodeAlpha Internship Assignment")
