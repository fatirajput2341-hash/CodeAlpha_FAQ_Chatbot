import streamlit as st
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize

# NLTK resources setup safely
@st.cache_resource
def download_nltk_resources():
    nltk.download('punkt')
    nltk.download('punkt_tab')

download_nltk_resources()

# UI Layout Settings
st.set_page_config(page_title="AI FAQ Chatbot", page_icon="🤖", layout="centered")

# --- UI Styling: ChatGPT Style Dark Theme & Fixed Input Visibility ---
st.markdown("""
    <style>
    /* ChatGPT Dark Background */
    .stApp { 
        background-color: #212121; 
        color: #ececec; 
    }
    /* Chat Input Container Styling */
    .stChatInputContainer { 
        border-radius: 24px !important; 
        border: 1px solid #4d4d4d !important; 
        background-color: #2f2f2f !important;
        padding: 4px 8px !important;
    }
    /* CRITICAL FIX: Make typed text 100% visible white and crisp */
    .stChatInputContainer textarea {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-size: 16px !important;
    }
    /* Placeholder Color */
    .stChatInputContainer textarea::placeholder {
        color: #b4b4b4 !important;
    }
    /* Titles and Text font adjustments */
    h1, h3, p, span { 
        color: #ececec !important; 
        font-family: 'Segoe UI', Inter, sans-serif; 
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Intelligent FAQ Chatbot")
st.write("Ask anything in any language (English, Urdu, Roman Urdu)...")

# --- Multi-Language FAQ Dataset (Expanded for better context matching) ---
faq_data = [
    {
        "keywords": ["return", "refund", "wapis", "chang", "vapis", "تبدیل", "واپس", "policy", "back"],
        "answer": "English: You can return any product within 30 days of purchase.\n\nRoman Urdu: Aap 30 din ke andar product wapis kar sakte hain.\n\nUrdu: آپ 30 دن کے اندر پروڈکٹ واپس کر سکتے ہیں۔"
    },
    {
        "keywords": ["shipping", "delivery", "time", "day", "kab", "milega", "pohanchega", "ڈلیوری", "دن", "shipped", "arrive", "deliv"],
        "answer": "English: Standard shipping takes 3-5 business days.\n\nRoman Urdu: Delivery me 3 se 5 din lagte hain.\n\nUrdu: ڈلیوری میں 3 سے 5 دن لگتے ہیں۔"
    },
    {
        "keywords": ["track", "order", "status", "check", "kahan hai", "ٹریک", "آرڈر", "tracking", "where"],
        "answer": "English: You will receive a tracking link via email once your order ships.\n\nRoman Urdu: Order ship hone ke baad aapko email par tracking link mil jayega.\n\nUrdu: آرڈر شپ ہونے کے بعد آپ کو ای میل پر ٹریکنگ لنک مل جائے گا۔"
    },
    {
        "keywords": ["payment", "pay", "card", "pese", "cash", "paisa", "ادائیگی", "پیسے", "money", "price", "fees", "cost"],
        "answer": "English: We accept Credit/Debit cards, PayPal, and Apple Pay.\n\nRoman Urdu: Hum Credit/Debit cards, PayPal aur Apple Pay accept karte hain.\n\nUrdu: ہم کریڈٹ/ڈیبٹ کارڈز، پے پال اور ایپل پے قبول کرتے ہیں۔"
    }
]

# Greetings Expanded Checklist
greetings_list = ["hello", "hi", "hey", "hloo", "hy", "asalam", "salam", "اؤ", "hlw", "helo", "yo"]

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

    # Smart Greetings Verification (Handles single words or slight variations)
    if any(greet in clean_input for greet in greetings_list) and len(user_words) <= 2:
        bot_reply = "Hello! How can I help you today? Ask me about our return policy, shipping, tracking, or payments.\n\n(Aap Urdu ya Roman Urdu me bhi pooch sakte hain!)"
    else:
        # --- Task 2: Match Logic ---
        best_match_idx = -1
        max_matches = 0
        
        for idx, faq in enumerate(faq_data):
            match_count = sum(1 for word in user_words if word in faq["keywords"])
            if match_count > max_matches:
                max_matches = match_count
                best_match_idx = idx

        if best_match_idx != -1 and max_matches > 0:
            bot_reply = faq_data[best_match_idx]["answer"]
        else:
            # Fallback Cosine Similarity mechanism
            all_questions = ["return policy refund change back", "shipping delivery time duration days arrive", "track order status package where", "payment options cash credit card money price cost"]
            all_texts = [clean_input] + all_questions
            
            try:
                vectorizer = TfidfVectorizer()
                tfidf_matrix = vectorizer.fit_transform(all_texts)
                scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
                best_idx = scores.argmax()
                
                # Dynamic Threshold match
                if scores[best_idx] > 0.12:
                    bot_reply = faq_data[best_idx]["answer"]
                else:
                    bot_reply = "English: Sorry, I couldn't find an answer to that in our FAQs.\n\nRoman Urdu: Maazrat, mujhe iska jawab FAQs me nahi mila. Kirpa karke shipping, return ya payment ke baare me poochein."
            except Exception:
                bot_reply = "Please ask a specific question about our services!"

    # Display Bot Reply
    with st.chat_message("assistant"):
        st.write(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
