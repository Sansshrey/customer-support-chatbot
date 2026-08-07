import json
from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent.parent



with open(
    BASE_DIR / "database/orders.json"
) as file:

    orders = json.load(file)




def get_order_status(order_id):


    for order in orders:


        if order["order_id"] == order_id:


            return {

                "found": True,

                "order_id": order["order_id"],

                "status": order["status"],

                "delivery": order["delivery"],

                "product": order["product"]

            }



    return {


        "found": False,

        "message":
        "Order not found"

    }