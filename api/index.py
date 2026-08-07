from flask import Flask, request, jsonify, render_template
import os
import sys


# Add project root path
sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)


from agents.root_agent import process_message

from utils.storage import (
    load_sessions,
    save_sessions,
    save_conversation
)



app = Flask(
    __name__,
    template_folder="../templates"
)



# Load saved user sessions

sessions = load_sessions()



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


    data = request.get_json()



    user_message = data.get(
        "message",
        ""
    )


    user_id = data.get(
        "user_id",
        "guest"
    )



    # Create session for new user

    if user_id not in sessions:


        sessions[user_id] = {


            "customer_id": None,

            "customer_name": None,

            "email": None,

            "auth_status": "not_verified",

            "pending_action": None,

            "waiting_for": None,

            "order_id": None,

            "transaction_id": None,

            "refund_id": None


        }



    # Send message to Root Agent

    response, intent = process_message(

        user_message,

        sessions[user_id]

    )



    # Save session memory

    save_sessions(
        sessions
    )


    print(
        "SESSION SAVED:",
        sessions[user_id]
    )



    # Save conversation logs

    save_conversation(

        user_id,

        user_message,

        intent,

        response

    )


    print(
        "CONVERSATION LOG SAVED"
    )



    return jsonify({

        "response": response,

        "intent": intent,

        "user_id": user_id

    })




if __name__ == "__main__":


    app.run(

        host="0.0.0.0",

        port=int(
            os.environ.get(
                "PORT",
                5000
            )
        )

    )