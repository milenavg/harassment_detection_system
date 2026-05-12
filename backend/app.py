from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import time
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
print("OPENAI KEY LOADED:", os.getenv("OPENAI_API_KEY") is not None)

# SIMPLE PROTECTION LAYERS

seen_cache = set()
last_request_time = 0
MIN_INTERVAL = 1.0  # 1 request / second

# SAFE OPENAI CALL 
def safe_moderation(text):
    for i in range(3):
        try:
            return client.moderations.create(
                model="omni-moderation-latest",
                input=text
            )
        except Exception as e:
            time.sleep(2 ** i)
    raise Exception("OpenAI request failed after retries")

# ROUTES
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Backend running"})


@app.route("/analyze", methods=["POST"])
def analyze():
    global last_request_time

    try:
        data = request.get_json()

        if not data or "text" not in data:
            return jsonify({"error": "No text provided"}), 400

        original_text = data["text"]
        cleaned_text = original_text.strip().lower()

        # RATE LIMIT (ANTI-SPAM)
        now = time.time()
        if now - last_request_time < MIN_INTERVAL:
            return jsonify({"status": "ignored (rate limit)"}), 200

        last_request_time = now

        # CACHE (ANTI-DUPLICATE)
        if cleaned_text in seen_cache:
            return jsonify({"status": "duplicate ignored"}), 200

        seen_cache.add(cleaned_text)

        # DEBUG LOG
        print("\n==============================")
        print("TEXT RECEIVED:")
        print(original_text)
        print("==============================\n")

        # OPENAI MODERATION
        moderation_response = safe_moderation(cleaned_text)

        result = moderation_response.results[0]
        category_scores = result.category_scores.model_dump()

        max_score = max(category_scores.values())
        score = round(float(max_score), 2)

        # LABEL LOGIC
        if score >= 0.70:
            label = "toxic"
        elif score >= 0.40:
            label = "suspicious"
        else:
            label = "safe"

        final_result = {
            "label": label,
            "score": score,
            "categories": result.categories
        }

        print("FINAL RESULT:")
        print(final_result)

        return jsonify(final_result)

    except Exception as error:
        print("SERVER ERROR:", error)

        return jsonify({
            "label": "error",
            "score": 0,
            "categories": {},
            "message": str(error)
        }), 500

# START SERVER
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )