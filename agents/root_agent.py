from agents.order_agent import handle_order
from agents.payment_agent import handle_payment
from agents.refund_agent import handle_refund
from agents.account_agent import handle_account
from agents.auth_agent import handle_auth



def detect_intent(message):

    text = message.lower().strip()


    if text in [
        "ok",
        "okay",
        "thanks",
        "thank you",
        "great",
        "got it"
    ]:

        return "confirmation"



    if text in [
        "no",
        "nope",
        "nothing"
    ]:

        return "goodbye"



    if any(word in text for word in [
        "track",
        "order",
        "delivery",
        "package"
    ]):

        return "order_tracking"



    if any(word in text for word in [
        "payment",
        "failed",
        "transaction",
        "charged"
    ]):

        return "payment_issue"



    if any(word in text for word in [
        "refund",
        "return",
        "money back"
    ]):

        return "refund_request"



    if any(word in text for word in [
        "password",
        "login",
        "account",
        "forgot"
    ]):

        return "account_issue"



    return "unknown"





def process_message(message, session):


    intent = detect_intent(message)



    # --------------------------
    # Confirmation
    # --------------------------

    if intent == "confirmation":

        return (

            "You're welcome. "
            "Is there anything else I can help you with?",

            "confirmation"

        )



    if intent == "goodbye":

        return (

            "Thank you for contacting Customer Support AI Agent. Have a great day!",

            "goodbye"

        )



    # --------------------------
    # Waiting for email
    # --------------------------

    if session.get("waiting_for") == "email":


        response = handle_auth(
            message,
            session
        )


        if session.get("auth_status") == "verified":


            session["waiting_for"] = (

                session.get(
                    "pending_action"
                )

            )


        return (

            response,

            "authentication"

        )




    # --------------------------
    # Waiting states
    # --------------------------


    if session.get("waiting_for") == "order_id":


        return (

            handle_order(
                message,
                session
            ),

            "order_id_received"

        )



    if session.get("waiting_for") == "transaction_id":


        return (

            handle_payment(
                message,
                session
            ),

            "transaction_id_received"

        )



    if session.get("waiting_for") == "refund_id":


        return (

            handle_refund(
                message,
                session
            ),

            "refund_id_received"

        )




    # --------------------------
    # Authentication requirement
    # --------------------------


    if intent in [
        "order_tracking",
        "refund_request"
    ]:


        if session.get(
            "auth_status"
        ) != "verified":


            session["waiting_for"] = "email"

            session["pending_action"] = intent


            return (

                "Before accessing your details, "
                "please provide your registered email address.",

                "authentication_required"

            )




    # --------------------------
    # Route agents
    # --------------------------


    if intent == "order_tracking":


        return (

            handle_order(
                message,
                session
            ),

            intent

        )



    if intent == "payment_issue":


        return (

            handle_payment(
                message,
                session
            ),

            intent

        )



    if intent == "refund_request":


        return (

            handle_refund(
                message,
                session
            ),

            intent

        )



    if intent == "account_issue":


        return (

            handle_account(
                message,
                session
            ),

            intent

        )



    return (

        "I can help you with orders, payments, refunds and account issues.",

        "unknown"

    )