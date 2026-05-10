from flask import Flask, request, jsonify

app = Flask(__name__)

# TODO:
# - receive text from extension
# - send to preprocessing + model
# - return result

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data["text"]

    # TODO: call model here
    result = {
        "label": "safe",
        "score": 0.1
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)