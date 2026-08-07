import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


with open(
    BASE_DIR / "database/customers.json"
) as file:

    customers = json.load(file)



def authenticate_user(email, session):


    for customer in customers:


        if customer["email"].lower() == email.lower():


            session["customer_id"] = customer["customer_id"]

            session["name"] = customer["name"]

            session["email"] = customer["email"]

            session["auth_status"] = "verified"


            return (

                True,

                f"Authentication successful. Welcome {customer['name']}."

            )



    return (

        False,

        "I could not verify your email. Please provide a registered email address."

    )





def handle_auth(message, session):


    email = message.strip()



    if "@" not in email:


        session["waiting_for"] = "email"


        return (

            "Please provide your registered email address."

        )



    success, response = authenticate_user(

        email,

        session

    )


    if success:

        session["waiting_for"] = None


    else:

        session["waiting_for"] = "email"



    return response