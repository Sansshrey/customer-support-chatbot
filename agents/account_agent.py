def handle_account(message, session):


    text = message.lower()



    if "password" in text or "forgot" in text:


        return (

            "To reset your password, "
            "open the login page and select "
            "'Forgot Password'. "
            "A reset link will be sent to your email."

        )



    return (

        "I can help with account login "
        "and password reset issues."

    )