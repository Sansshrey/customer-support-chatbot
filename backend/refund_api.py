import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


with open(
    BASE_DIR / "database/refunds.json",
    encoding="utf-8"
) as file:

    refunds = json.load(file)




def get_refund_status(refund_id):


    for refund in refunds:


        if refund["refund_id"] == refund_id:


            return {

                "found": True,
                "status": refund["status"],
                "amount": refund["amount"],
                "days": refund["days"]

            }



    return {

        "found": False

    }