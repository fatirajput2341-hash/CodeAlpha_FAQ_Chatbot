import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app)  # Is se frontend connection block nahi hoga

# Apni Gemini API Key yahan dalein ya system environment variable set karein
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_ACTUAL_GEMINI_API_KEY_HERE")

# Google Gen AI Client Initialize karein
client = genai.Client(api_key=GEMINI_API_KEY)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400

        # Gemini model se response generate karein
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
        )

        return jsonify({'reply': response.text})

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

if __name__ == '__main__':
    # Default Flask port 5000 par chalega
    app.run(host='0.0.0.0', port=5000, debug=True)
