import os
import streamlit as st
from google import genai
from google.genai import types

# Page Configurations (Title aur Icon)
st.set_page_config(page_title="AI FAQ Chatbot", page_icon="🤖", layout="centered")

# --- UI Styling: Professional Dark/Clean UI ---
st.markdown("""
    <style>
    /* Main Background color */
    .stApp {
        background-color: #141d26;
        color: #ffffff;
    }
    /* Input Box Styling */
    .stChatInputContainer {
        border-radius: 10px;
        border: 1px solid #1da1f2;
    }
    /* Titles styling */
    h1, h3, p {
        color: #ffffff !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Intelligent FAQ Chatbot")
st.write("Ask anything in any language (English, Urdu, Roman Urdu)...")

# --- Gemini API Client Setup ---
# Apni Gemini API Key yahan enter karein (Ya environment variable set karein)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_ACTUAL_GEMINI_API_KEY_HERE")
client = genai.Client(api_key=GEMINI_API_KEY)

# --- Task 2: System Instructions for FAQ & Multi-language ---
system_instruction = """
You are an expert FAQ Chatbot for a product/service. 
Your primary task is to match user questions with the company's FAQ knowledge base.
FAQs Context:
- Return Policy: 30 days of purchase, money-back guarantee.
- Shipping: Standard takes 3-5 business days. International shipping is available with extra charges.
- Order Tracking: Tracking link sent via email after shipment.
- Payment Methods: Credit/Debit cards, PayPal, Apple Pay.

CRITICAL RULES:
1. The user can ask questions in English, Urdu (Urdu script), or Roman Urdu/Hinglish (e.g., 'delivery kitni der me hogi?', 'pese kese dene hain?', 'hloo').
2. Always detect the user's language and reply in the EXACT SAME language/style they used. If they ask in Roman Urdu, reply in Roman Urdu. If they say 'hloo/hi', greet them friendly.
3. If the question is completely outside these FAQs, politely tell them that you only handle product FAQs.
"""

# Streamlit Session State for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User Input Field
if user_message := st.chat_input("Ask anything in any language..."):
    # Display User Message
    with st.chat_message("user"):
        st.write(user_message)
    st.session_state.messages.append({"role": "user", "content": user_message})

    # Call Gemini API with System Instructions
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.3 # Low temperature keeps it focused on FAQs
            )
        )
        bot_reply = response.text
    except Exception as e:
        bot_reply = "Connection is adjusting. Please type your query once more!"
        print(f"Error: {e}")

    # Display Bot Response
    with st.chat_message("assistant"):
        st.write(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
