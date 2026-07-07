import streamlit as st
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# NLTK resources download karne ka updated function
@st.cache_resource
def download_nltk_resources():
    nltk.download('punkt')
    nltk.download('punkt_tab')  # Fixed line
    nltk.download('stopwords')
    nltk.download('wordnet')

download_nltk_resources()

# Page UI Config
st.set_page_config(page_title="FAQ Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 NLP FAQ Chatbot")
st.write("Ask any question related to our services!")

# 1. FAQ Data: Questions aur unke Answers
faq_data = [
    {"question": "What is your return policy?", "answer": "You can return any product within 30 days of purchase."},
    {"question": "How long does shipping take?", "answer": "Standard shipping takes 3-5 business days."},
    {"question": "How can I track my order?", "answer": "You will receive a tracking link via email once your order ships."},
    {"question": "Do you offer international shipping?", "answer": "Yes, we ship worldwide with additional shipping charges."},
    {"question": "What payment methods do you accept?", "answer": "We accept Credit/Debit cards, PayPal, and Apple Pay."}
]
faq_questions = [item["question"] for item in faq_data]

# 2. Text Preprocessing Function (Using NLTK)
def preprocess_text(text):
    text = text.lower()
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    
    cleaned_tokens = [
        lemmatizer.lemmatize(word) 
        for word in tokens 
        if word.isalnum() and word not in stop_words
    ]
    return " ".join(cleaned_tokens)

# Streamlit Chat History Maintain karne ke liye
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purane messages display karne ke liye
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input text box
if user_message := st.chat_input("Type your question here..."):
    # User message display karein
    with st.chat_message("user"):
        st.write(user_message)
    st.session_state.messages.append({"role": "user", "content": user_message})

    # --- NLP Cosine Similarity Logic ---
    processed_user_msg = preprocess_text(user_message)
    processed_faqs = [preprocess_text(q) for q in faq_questions]
    all_texts = [processed_user_msg] + processed_faqs

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    # User vs FAQs Similarity Matrix
    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
    best_match_idx = similarity_scores.argmax()
    highest_score = similarity_scores[best_match_idx]

    # Threshold check
    if highest_score > 0.2:
        bot_reply = faq_data[best_match_idx]["answer"]
    else:
        bot_reply = "Sorry, I couldn't find an answer to that in our FAQs. Please ask something else!"

    # Bot response display karein
    with st.chat_message("assistant"):
        st.write(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
