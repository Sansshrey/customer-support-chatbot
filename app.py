from flask import Flask, render_template, request, jsonify
import json
import re
import string
import random
from datetime import datetime

app = Flask(__name__)

# Load intents from JSON file

with open("intents.json", "r") as f:
    data = json.load(f)

INTENTS = data["intents"]


# Session memory
# stores last intent per user

last_intent = {"tag": None}


# NLP Preprocessing

STOPWORDS = {
    "is", "the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
    "for", "of", "with", "my", "me", "i", "it", "this", "that", "was",
    "are", "be", "been", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "shall", "can", "not",
    "no", "yes", "please", "help", "want", "need", "get", "how", "what",
    "when", "where", "who", "why", "your", "our", "their", "its", "we"
}

def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = text.split()
    tokens = [w for w in tokens if w not in STOPWORDS]
    return tokens


# Intent Detection

def detect_intent(user_input):
    text_lower = user_input.lower()
    tokens = preprocess(user_input)

    # Check if user entered an ID (alphanumeric code)
    if re.match(r'^[A-Za-z0-9]{4,}$', user_input.strip()):

        # If last intent was payment — this is a transaction ID
        if last_intent["tag"] == "payment_issues":
            return "transaction_id_received"

        # If last intent was order tracking — this is a tracking ID
        if last_intent["tag"] == "order_tracking":
            return "tracking_id_received"

        # Otherwise generic ID response
        return "tracking_id_received"

    best_tag = "unknown"
    best_score = 0

    for intent in INTENTS:
        score = 0
        for pattern in intent["patterns"]:
            pattern_tokens = preprocess(pattern)
            matches = sum(1 for t in pattern_tokens if t in tokens)
            if matches > 0:
                score += matches * 2
            if pattern.lower() in text_lower:
                score += 3
        if score > best_score:
            best_score = score
            best_tag = intent["tag"]

    return best_tag if best_score >= 1 else "unknown"

# Get Response

UNKNOWN_RESPONSES = [
    "I am sorry, I did not understand that. Could you rephrase your question?",
    "I am not sure about that. Please contact support@company.com for help.",
    "That is outside my knowledge. Try asking about orders, refunds, payments or login issues."
]

TRANSACTION_RESPONSES = [
    "Thank you for sharing your transaction ID. Our billing team has been notified and will resolve your payment issue within 24 hours. You will receive a confirmation email shortly.",
    "Got your transaction ID! Our billing team will investigate the payment failure and process any refund if applicable within 3 to 5 business days.",
    "Thank you! We have recorded your transaction ID. If money was deducted, it will be refunded automatically within 3 to 5 business days."
]

TRACKING_RESPONSES = [
    "Thank you for sharing your tracking ID. Your order is currently being processed and will be delivered within 2 to 3 business days.",
    "Got your tracking ID! Your package is out for delivery. You will receive an SMS update shortly.",
    "Thank you! Your order has been dispatched and is expected to arrive by tomorrow."
]

def get_response(tag):
    if tag == "transaction_id_received":
        return random.choice(TRANSACTION_RESPONSES)
    if tag == "tracking_id_received":
        return random.choice(TRACKING_RESPONSES)
    for intent in INTENTS:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])
    return random.choice(UNKNOWN_RESPONSES)

# Save chat log to file

def save_log(user_msg, bot_reply, tag):
    with open("chat_logs.txt", "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] USER: {user_msg}\n")
        f.write(f"[{timestamp}] BOT [{tag}]: {bot_reply}\n")
        f.write("-" * 50 + "\n")

# Flask Routes

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    tag = detect_intent(user_message)
    response = get_response(tag)

    # Remember this intent for next message
    last_intent["tag"] = tag

    save_log(user_message, response, tag)
    return jsonify({
        "response": response,
        "intent": tag
    })

if __name__ == "__main__":
    app.run(debug=True)
