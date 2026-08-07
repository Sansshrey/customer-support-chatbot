from backend.refund_api import get_refund_status



def handle_refund(message, session):


    if session.get("waiting_for") == "refund_id":


        refund_id = message.strip()


        session["refund_id"] = refund_id

        session["waiting_for"] = None


        result = get_refund_status(
            refund_id
        )


        if result["found"]:


            return (

                f"Refund {refund_id} is "
                f"{result['status']}. "
                f"Amount: {result['amount']}. "
                f"Expected time: {result['days']}."

            )


        return (

            "I could not find this refund ID."

        )



    session["waiting_for"] = "refund_id"


    return (

        "Please provide your refund ID "
        "to check refund status."

    )