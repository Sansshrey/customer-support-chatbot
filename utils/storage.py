import json
import os
from datetime import datetime


# In-memory storage for Vercel
sessions = {}

conversations = []


def load_sessions():

    return sessions



def save_sessions(data):

    global sessions

    sessions = data

    return True



def get_user_session(user_id):

    if user_id not in sessions:

        sessions[user_id] = {

            "authenticated": False,
            "name": None,
            "email": None,
            "current_intent": None,
            "order_id": None,
            "transaction_id": None,
            "refund_id": None

        }

    return sessions[user_id]



def update_user_session(user_id, key, value):

    session = get_user_session(user_id)

    session[key] = value

    sessions[user_id] = session

    return session



# Keep this because index.py imports it

def save_conversation(
        user_id,
        user_message,
        bot_response,
        intent
):

    conversations.append({

        "user_id": user_id,

        "user_message": user_message,

        "bot_response": bot_response,

        "intent": intent,

        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    })

    return True



def get_conversations():

    return conversations