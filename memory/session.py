# Session Memory Manager
# Similar to CX Agent Studio Session Parameters


sessions = {}



def create_session(user_id):

    if user_id not in sessions:

        sessions[user_id] = {


            # Customer Information

            "customer_id": None,

            "name": None,

            "email": None,



            # Authentication

            "auth_status": "not_verified",



            # Conversation State

            "intent": None,

            "waiting_for": None,



            # Business Parameters

            "order_id": None,

            "transaction_id": None,

            "refund_id": None


        }


    return sessions[user_id]




def get_session(user_id):

    return sessions.get(
        user_id
    )




def update_session(
        user_id,
        key,
        value
):

    if user_id not in sessions:

        create_session(
            user_id
        )


    sessions[user_id][key] = value