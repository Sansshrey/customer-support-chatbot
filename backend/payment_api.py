import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


with open(
    BASE_DIR / "database/payments.json",
    encoding="utf-8"
) as file:

    payments = json.load(file)




def get_payment_status(transaction_id):


    for payment in payments:


        if payment["transaction_id"] == transaction_id:


            return {

                "found": True,
                "status": payment["status"],
                "amount": payment["amount"],
                "message": payment["message"]

            }


    return {

        "found": False,
        "message": "Transaction not found"

    }