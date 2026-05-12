from flask import Flask, request, jsonify
from flask_cors import CORS

from rule_engine import analyze_text
from features_mapper import map_c_features

app = Flask(__name__)
CORS(app)  # allow extension to call backend

@app.route("/")
def home():
    return "Harassment Detection API is running"

@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({
            "label": "error",
            "score": 0,
            "categories": {}
        }), 400

    text = data["text"]

    # 1. C MODULE FEATURE EXTRACTION
    c_features = map_c_features(text)

    # 2. RULE ENGINE (PYTHON LOGIC)
    result = analyze_text(text, c_features)

    # 3. RESPONSE TO EXTENSION
    return jsonify(result)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    print("Flask backend running on http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)