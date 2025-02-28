from flask import Flask, request, jsonify,render_template
import openai
import os
from google.cloud import speech_v1p1beta1 as speech
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()


app = Flask(__name__)
CORS(app)

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/translate", methods=["POST"])
def translate_text():
    data = request.json
    text = data.get("text")
    target_language = data.get("target_language", "es")  # Default to Spanish

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # Correct OpenAI API call
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Translate the following text to {target_language}:"},
                {"role": "user", "content": text},
            ],
            max_tokens=100,
        )

        translated_text = response.choices[0].message.content.strip()

        return jsonify({"translated_text": translated_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)