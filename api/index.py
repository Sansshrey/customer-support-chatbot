from flask import Flask, render_template, request, jsonify
import json
import re
import string
import random
import os
from datetime import datetime
from pathlib import Path


app = Flask(
    __name__,
    template_folder="../templates"
)


# -----------------------------
# Load intents.json
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR / "intents.json", "r") as f:
    data = json.load(f)


INTENTS = data["intents"]


# -----------------------------
# User session memory
# -----------------------------

sessions = {}



# -----------------------------
# NLP preprocessing
# -----------------------------

STOPWORDS = {
    "is", "the", "a", "an", "and", "or", "but",
    "in", "on", "at", "to", "for", "of",
    "with", "my", "me", "i", "it", "this",
    "that", "was", "are", "be", "been",
    "have", "has", "had", "do", "does",
    "did", "will", "would", "could",
    "should", "may", "might", "can",
    "not", "no", "yes", "please",
    "help", "want", "need", "get",
    "how", "what", "when", "where",
    "who", "why", "your", "our",
    "their", "its", "we"
}



def preprocess(text):

    text = text.lower()

    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    tokens = text.split()


    tokens = [
        word for word in tokens
        if word not in STOPWORDS
    ]

    return tokens



# -----------------------------
# Intent Detection
# -----------------------------

def detect_intent(user_input, user_id):

    text_lower = user_input.lower()

    tokens = preprocess(user_input)


    previous_intent = (
        sessions.get(user_id, {})
        .get("last_intent")
    )


    # Detect IDs

    if re.match(
        r"^[A-Za-z0-9]{4,}$",
        user_input.strip()
    ):

        if previous_intent == "payment_issues":
            return "transaction_id_received"


        if previous_intent == "order_tracking":
            return "tracking_id_received"


        return "tracking_id_received"



    best_tag = "unknown"

    best_score = 0



    for intent in INTENTS:

        score = 0


        for pattern in intent["patterns"]:

            pattern_tokens = preprocess(pattern)


            matches = sum(
                1
                for token in pattern_tokens
                if token in tokens
            )


            if matches > 0:
                score += matches * 2


            if pattern.lower() in text_lower:
                score += 3



        if score > best_score:

            best_score = score
            best_tag = intent["tag"]



    if best_score >= 1:

        return best_tag


    return "unknown"



# -----------------------------
# Responses
# -----------------------------


UNKNOWN_RESPONSES = [

    "I am sorry, I did not understand that. Could you rephrase your question?",

    "I am not sure about that. Please contact support for further assistance.",

    "I can help with orders, payments, refunds and login issues."

]



TRANSACTION_RESPONSES = [

    "Thank you for sharing your transaction ID. Our billing team has been notified and will resolve your payment issue within 24 hours.",

    "Got your transaction ID. Our billing team will investigate and process any refund if applicable.",

    "Your transaction ID has been recorded. Refunds are processed within 3 to 5 business days."

]



TRACKING_RESPONSES = [

    "Thank you for sharing your tracking ID. Your order is currently being processed.",

    "Got your tracking ID. Your package status has been updated.",

    "Your order has been dispatched and will arrive soon."

]



def get_response(tag):


    if tag == "transaction_id_received":

        return random.choice(
            TRANSACTION_RESPONSES
        )



    if tag == "tracking_id_received":

        return random.choice(
            TRACKING_RESPONSES
        )



    for intent in INTENTS:

        if intent["tag"] == tag:

            return random.choice(
                intent["responses"]
            )


    return random.choice(
        UNKNOWN_RESPONSES
    )



# -----------------------------
# Logging
# Vercel compatible
# -----------------------------

def save_log(
        user_msg,
        bot_reply,
        tag,
        user_id
):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    print(
        f"""
[{timestamp}]
USER {user_id}: {user_msg}

BOT [{tag}]: {bot_reply}

------------------------
"""
    )



# -----------------------------
# Routes
# -----------------------------


@app.route("/")
def home():

    return render_template(
        "index.html"
    )



@app.route(
    "/chat",
    methods=["POST"]
)
def chat():

    data = request.json


    user_message = data.get(
        "message",
        ""
    )


    user_id = data.get(
        "user_id",
        "guest"
    )



    if user_id not in sessions:

        sessions[user_id] = {
            "last_intent": None
        }



    tag = detect_intent(
        user_message,
        user_id
    )


    response = get_response(
        tag
    )


    sessions[user_id]["last_intent"] = tag



    save_log(
        user_message,
        response,
        tag,
        user_id
    )



    return jsonify({

        "response": response,

        "intent": tag,

        "user_id": user_id

    })



# Vercel needs this
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )