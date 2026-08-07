from backend.payment_api import get_payment_status

def handle_payment(message, session):


    if session.get("waiting_for") == "transaction_id":


        transaction_id = message.strip()


        session["transaction_id"] = transaction_id

        session["waiting_for"] = None



        result = get_payment_status(
            transaction_id
        )


        if result["found"]:


            return (

                f"Transaction {transaction_id} "
                f"status: {result['status']}. "
                f"Amount: {result['amount']}. "
                f"{result['message']}"

            )


        return (

            "I could not find this transaction ID."

        )




    session["waiting_for"] = "transaction_id"



    return (

        "Please provide your transaction ID "
        "to check payment status."

    )