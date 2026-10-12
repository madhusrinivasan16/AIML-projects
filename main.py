
from flask import Flask, render_template, request, jsonify
from service import get_ai_response

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}

    message = data.get("message", "").strip()
    history = data.get("history", [])

    if not message:
        return jsonify({"error": "Please enter a message."}), 400

    if not isinstance(message, str) or len(message) > 5000:
        return jsonify({"error": "Message must be under 5000 characters."}), 400

    if not isinstance(history, list):
        history = []

    safe_history = []
    for item in history[-10:]:
        if (
            isinstance(item, dict)
            and item.get("role") in ("user", "assistant")
            and isinstance(item.get("content"), str)
        ):
            safe_history.append({
                "role": item["role"],
                "content": item["content"][:5000]
            })

    try:
        answer = get_ai_response(message, safe_history)
        return jsonify({"reply": answer})

    except Exception:
        app.logger.exception("Gemini request failed")
        return jsonify({
            "error": "AI service failed. Check your API key, "
                     "internet connection, model access and quota."
        }), 502


if __name__ == "__main__":
    app.run(debug=True)