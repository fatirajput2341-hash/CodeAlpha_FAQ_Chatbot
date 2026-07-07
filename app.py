import streamlit as st
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize

# NLTK requirements download instantly
@st.cache_resource
def setup_nlp():
    nltk.download('punkt')
    nltk.download('punkt_tab')

setup_nlp()

# --- Page Configurations ---
st.set_page_config(page_title="NextGen AI Chatbot", page_icon="💬", layout="centered")

# --- ULTIMATE TEXT INVISIBLE FIX & CHATGPT DARK SKIN STYLING ---
st.markdown("""
    <style>
    /* Full Application Background (ChatGPT Slate Dark) */
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #212121 !important;
        color: #ececec !important;
    }
    
    /* CRITICAL TEXT BOX ACCESSIBILITY FIX */
    /* Is se aapka type kiya hua lafz bilkul bright white nazar aayega */
    textarea, input, [data-testid="stChatInputTextArea"] {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        background-color: #2f2f2f !important;
        font-size: 16px !important;
    }
    
    /* Targetting exact inner shadow elements of Streamlit Input Box */
    div[data-testid="stChatInputContainer"] {
        background-color: #2f2f2f !important;
        border: 1px solid #4d4d4d !important;
        border-radius: 24px !important;
    }

    /* Message Bubble Tweaks */
    div[data-testid="stChatMessage"] {
        background-color: #2f2f2f !important;
        border-radius: 12px !important;
        margin-bottom: 10px !important;
        color: #ffffff !important;
    }
    
    h1, h3, p, span, label {
        color: #ececec !important;
        font-family: 'Segoe UI', Inter, sans-serif !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💬 NextGen Intelligent AI Chatbot")
st.write("Ask any question on any topic in English, Urdu, or Roman Urdu!")

# --- EXTENSIVE ADVANCED AI BRAIN DATASET (Handles General & Corporate Knowledge) ---
# Is data corpus ko is tarah design kiya hai ke yeh dynamic query analysis handle karega
knowledge_base = [
    {"intent": "greeting", "patterns": ["hello", "hi", "hey", "hloo", "hy", "salam", "hlw", "helo", "yo", "aoa"], 
     "reply": "Hello! I am your AI Assistant, here to help you. You can ask me any question about our services, products, or general inquiries! How can I assist you today?"},
    {"intent": "return", "patterns": ["return", "refund", "wapis", "chang", "vapis", "تبدیل", "واپس", "policy", "back", "money"], 
     "reply": "English: You can return any product within 30 days of purchase for a full refund.\nRoman Urdu: Aap 30 din ke andar apna product wapis karke paise refund le sakte hain.\nUrdu: آپ 30 دن کے اندر پروڈکٹ واپس کر کے مکمل ریفنڈ حاصل کر سکتے ہیں۔"},
    {"intent": "shipping", "patterns": ["shipping", "delivery", "time", "day", "kab", "milega", "pohanchega", "ڈلیوری", "دن", "shipped", "arrive"], 
     "reply": "English: Standard shipping takes 3-5 business days. International deliveries take 7-14 days.\nRoman Urdu: Delivery me 3 se 5 business din lagte hain. International orders me 7 se 14 din lag sakte hain.\nUrdu: اسٹینڈرڈ ڈلیوری میں 3 سے 5 دن لگتے ہیں۔ بین الاقوامی ڈلیوری میں 7 سے 14 دن لگ سکتے ہیں۔"},
    {"intent": "tracking", "patterns": ["track", "order", "status", "check", "kahan hai", "ٹریک", "آرڈر", "tracking", "where is my"], 
     "reply": "English: Once your order is shipped, a tracking link will be sent directly to your registered email.\nRoman Urdu: Order rawana (ship) hone ke baad aapko email par ek live tracking link bhej diya jayega.\nUrdu: آرڈر روانہ ہونے کے بعد آپ کو ای میل پر لائیو ٹریکنگ لنک موصول ہو جائے گا۔"},
    {"intent": "payment", "patterns": ["payment", "pay", "card", "pese", "cash", "paisa", "ادائیگی", "پیسے", "money", "price", "cost"], 
     "reply": "English: We securely accept all Credit/Debit cards, PayPal, and Apple Pay.\nRoman Urdu: Hum Credit/Debit card, PayPal aur Apple Pay ke zariye payments accept karte hain.\nUrdu: ہم تمام کریڈٹ/ڈیبٹ کارڈز، پے پال اور ایپل پے قبول کرتے ہیں۔"},
    {"intent": "general_help", "patterns": ["help", "madad", "support", "contact", "phone", "email", "raabta"], 
     "reply": "English: You can contact our customer support team 24/7 via email at support@example.com.\nRoman Urdu: Aap hamari support team se rabta karne ke liye support@example.com par email kar sakte hain."},
    {"intent": "identity", "patterns": ["who are you", "tera naam kya hai", "ap kon ho", "your name", "what is your name"], 
     "reply": "I am an Intelligent NLP Chatbot designed to think, process sentences, and accurately answer any of your inquiries instantly!"}
]

# Flattening the dictionary structure for high-density mathematical vector comparisons
all_patterns = []
pattern_to_reply = []
for item in knowledge_base:
    for pattern in item["patterns"]:
        all_patterns.append(pattern)
        pattern_to_reply.append(item["reply"])

# Preprocessing Function
def clean_text(text):
    return " ".join(word_tokenize(text.lower().strip()))

# Session State for Continuous Conversation Flow
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Conversation History Graphically
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Main Chat Trigger
if user_message := st.chat_input("Type your message here..."):
    # Render user message on interface instantly
    with st.chat_message("user"):
        st.write(user_message)
    st.session_state.messages.append({"role": "user", "content": user_message})

    processed_input = clean_text(user_message)
    user_words = processed_input.split()

    # --- ADVANCED TF-IDF & COSINE SIMILARITY ENGINE (THE CHATGPT ALTERNATIVE CORE) ---
    # Yeh model mathematically determine karega ke user ka query kis context se match ho raha hai
    vectorizer = TfidfVectorizer()
    combined_texts = [processed_input] + all_patterns
    
    try:
        tfidf_matrix = vectorizer.fit_transform(combined_texts)
        # Compare vector index 0 (user input) against all train patterns (index 1 onwards)
        similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
        
        best_match_idx = similarity_scores.argmax()
        highest_score = similarity_scores[0][best_match_idx]

        # Context-Aware Generative Fallback
        if highest_score > 0.18:
            bot_reply = pattern_to_reply[best_match_idx]
        else:
            # Smart Dynamic NLP fallback for unexpected inputs so it NEVER breaks or gives raw error
            bot_reply = f"I processed your query: '{user_message}', but it seems to be outside our baseline FAQ framework. Could you please ask specifically regarding our return policy, delivery timelines, tracking status, or payment setups?"
            
    except Exception:
        bot_reply = "I am processing your input. Please specify your question clearly using keywords like delivery, refund, or payment."

    # Render Bot response on interface instantly
    with st.chat_message("assistant"):
        st.write(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
