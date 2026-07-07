import streamlit as st
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize

# NLTK resources setup
@st.cache_resource
def download_nltk_resources():
    nltk.download('punkt')
    nltk.download('punkt_tab')

download_nltk_resources()

# UI Layout Settings
st.set_page_config(page_title="AI FAQ Chatbot", page_icon="🤖", layout="centered")

# --- UI Styling: Professional Dark/Clean UI ---
st.markdown("""
    <style>
    .stApp { background-color: #141d26; color: #ffffff; }
    .stChatInputContainer { border-radius: 10px; border: 1px solid #1da1f2; }
    h1, h3, p { color: #ffffff !important; font-family: 'Segoe UI', sans-serif; }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Intelligent FAQ Chatbot")
st.write("Ask anything in any language (English, Urdu, Roman Urdu)...")

# --- Task 2: Multi-Language FAQ Dataset (English, Urdu, Roman Urdu mapping) ---
faq_data = [
    {
        "keywords": ["return", "refund", "wapis", "chang", "vapis", "تبدیل", "واپس"],
        "answer": "English: You can return any product within 30 days of purchase.\n\nRoman Urdu: Aap 30 din ke andar product wapis kar sakte hain.\n\nUrdu: آپ 30 دن کے اندر پروڈکٹ واپس کر سکتے ہیں۔"
    },
    {
        "keywords": ["shipping", "delivery", "time", "day", "kab", "milega", "pohanchega", "ڈلیوری", "دن"],
        "answer": "English: Standard shipping takes 3-5 business days.\n\nRoman Urdu: Delivery me 3 se 5 din lagte hain.\n\nUrdu: ڈلیوری میں 3 سے 5 دن لگتے ہیں۔"
    },
    {
        "keywords": ["track", "order", "status", "check", "kahan hai", "ٹریک", "آرڈر"],
        "answer": "English: You will receive a tracking link via email once your order ships.\n\nRoman Urdu: Order ship hone ke baad aapko email par tracking link mil jayega.\n\nUrdu: آرڈر شپ ہونے کے بعد آپ کو ای میل پر ٹریکنگ لنک مل جائے گا۔"
    },
    {
        "keywords": ["payment", "pay", "card", "pese", "cash", "paisa", "ادائیگی", "پیسے"],
        "answer": "English: We accept Credit/Debit cards, PayPal, and Apple Pay.\n\nRoman Urdu: Hum Credit/Debit cards, PayPal aur Apple Pay accept karte hain.\n\nUrdu: ہم کریڈٹ/ڈیبٹ کارڈز، پے پال اور ایپل پے قبول کرتے ہیں۔"
    }
]

# Preprocessing for matching
def simple_clean(text):
    return " ".join(word_tokenize(text.lower().strip()))

# Session State for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User Chat Input
if user_message := st.chat_input("Ask anything in any language..."):
    with st.chat_message("user"):
        st.write(user_message)
    st.session_state.messages.append({"role": "user", "content": user_message})

    clean_input = simple_clean(user_message)
    user_words = clean_input.split()

    # Greetings Handle Karna
    if clean_input in ["hello", "hi", "hey", "hloo", "hy", "asalam", "salam", "اؤ"]:
        bot_reply = "Hello! How can I help you today? Ask me about our return policy, shipping, tracking, or payments.\n\n(Aap Urdu ya Roman Urdu me bhi pooch sakte hain!)"
    else:
        # --- Task 2: Advanced NLP Match Logic ---
        best_match_idx = -1
        max_matches = 0
        
        # Keyword context score base calculation
        for idx, faq in enumerate(faq_data):
            match_count = sum(1 for word in user_words if word in faq["keywords"])
            if match_count > max_matches:
                max_matches = match_count
                best_match_idx = idx

        if best_match_idx != -1 and max_matches > 0:
            bot_reply = faq_data[best_match_idx]["answer"]
        else:
            # Fallback Cosine Similarity mechanism if keyword fallback is deep
            all_questions = ["return policy refund change", "shipping delivery time duration days", "track order status package", "payment options cash credit card money"]
            all_texts = [clean_input] + all_questions
            
            try:
                vectorizer = TfidfVectorizer()
                tfidf_matrix = vectorizer.fit_transform(all_texts)
                scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
                best_idx = scores.argmax()
                
                if scores[0][best_idx] > 0.15:
                    bot_reply = faq_data[best_idx]["answer"]
                else:
                    bot_reply = "English: Sorry, I couldn't find an answer to that in our FAQs.\n\nRoman Urdu: Maazrat, mujhe iska jawab FAQs me nahi mila. Kirpa karke shipping, return ya payment ke baare me poochein."
            except Exception:
                bot_reply = "Please ask a specific question about our services!"

    # Display Bot Reply
    with st.chat_message("assistant"):
        st.write(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
