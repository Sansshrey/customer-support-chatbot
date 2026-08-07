from backend.order_api import get_order_status



def handle_order(message, session):


    # If waiting for order id

    if session.get("waiting_for") == "order_id":


        order_id = message.strip()


        session["order_id"] = order_id

        session["waiting_for"] = None



        result = get_order_status(
            order_id
        )


        if result["found"]:


            return (

                f"Hello {session.get('name')}. "
                f"Your order {result['order_id']} "
                f"is {result['status']}. "
                f"Expected delivery: {result['delivery']}."

            )


        else:


            return (

                "I could not find this order ID. "
                "Please check your order ID and try again."

            )




    # First time order request


    session["waiting_for"] = "order_id"



    return (

        "I can help you track your order. "
        "Please provide your order ID."

    )