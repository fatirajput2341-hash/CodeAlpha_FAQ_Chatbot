import os
import nltk
from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# NLTK resources download karna zaroori hai text preprocessing ke liye
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

app = Flask(__name__)
CORS(app)

# 1. FAQ Data: Questions aur unke Answers ka dictionary
faq_data = [
    {"question": "What is your return policy?", "answer": "You can return any product within 30 days of purchase."},
    {"question": "How long does shipping take?", "answer": "Standard shipping takes 3-5 business days."},
    {"question": "How can I track my order?", "answer": "You will receive a tracking link via email once your order ships."},
    {"question": "Do you offer international shipping?", "answer": "Yes, we ship worldwide with additional shipping charges."},
    {"question": "What payment methods do you accept?", "answer": "We accept Credit/Debit cards, PayPal, and Apple Pay."}
]

# FAQs se sirf questions alag nikalne ke liye list
faq_questions = [item["question"] for item in faq_data]

# 2. Text Preprocessing Function (Using NLTK)
def preprocess_text(text):
    # Lowercase karna
    text = text.lower()
    # Tokenization
    tokens = word_tokenize(text)
    # Stopwords (faltu words) hatana aur Lemmatization (base words nikalna)
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    
    cleaned_tokens = [
        lemmatizer.lemmatize(word) 
        for word in tokens 
        if word.isalnum() and word not in stop_words
    ]
    return " ".join(cleaned_tokens)

# 3. Chat Route
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({'reply': 'Please type a question!'})

        # Preprocess both user question and FAQ questions
        processed_user_msg = preprocess_text(user_message)
        processed_faqs = [preprocess_text(q) for q in faq_questions]

        # All questions ko combine karna vectorization ke liye
        all_texts = [processed_user_msg] + processed_faqs

        # TF-IDF Vectorizer to convert text to numbers
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(all_texts)

        # Cosine Similarity calculate karna (User question vs All FAQs)
        # tfidf_matrix[0:1] user ka vector hai, baqi FAQs ke vectors hain
        similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])

        # Sab se zyada match hone wale score ka index nikalna
        best_match_idx = similarity_scores.argmax()
        highest_score = similarity_scores[0][best_match_idx]

        # Agar matching score 0.2 se zyada hai to answer return karein, warna fallback message
        if highest_score > 0.2:
            matched_answer = faq_data[best_match_idx]["answer"]
            return jsonify({'reply': matched_answer})
        else:
            return jsonify({'reply': "Sorry, I couldn't find an answer to that in our FAQs. Please ask something else!"})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'reply': 'Connection error or server issue occurred.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
