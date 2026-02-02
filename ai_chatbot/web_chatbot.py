# from flask import Flask, render_template, request, jsonify
# import random

# app = Flask(__name__)

# def bot_reply(user_msg):
#     replies = [
#         "That's interesting! Tell me more.",
#         "I understand, my friend.",
#         "Nice! What do you want to do next?",
#         "I'm here to help you.",
#         "Can you explain that a little more?"
#     ]

#     msg = user_msg.lower()

#     if "hello" in msg:
#         return "Hello my friend! How are you?"
#     elif "name" in msg:
#         return "I am your personal voice enabled AI chatbot."
#     elif "bye" in msg:
#         return "Goodbye my friend! Have a great day."
#     else:
#         return random.choice(replies)

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/chat", methods=["POST"])
# def chat():
#     data = request.get_json()
#     user_message = data.get("message", "")
#     reply = bot_reply(user_message)
#     return jsonify({"reply": reply})

# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=5000, debug=True)


from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Load API Key
def load_api_key():
    try:
        with open("ai_bot_api_key.txt", "r") as f:
            return f.read().strip()
    except:
        return None

API_KEY = load_api_key()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")

    if not user_msg:
        return jsonify({"reply": "Please type a message."})

    # Simple local AI logic (no OpenAI)
    reply = f"You said: {user_msg}"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    print("🌐 Website Chatbot Running...")
    print("Open in browser: http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
