import json
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent


STORAGE_DIR = BASE_DIR / "storage"


SESSION_FILE = STORAGE_DIR / "sessions.json"

LOG_FILE = STORAGE_DIR / "conversations.json"



# Create storage folder automatically

STORAGE_DIR.mkdir(
    exist_ok=True
)



def load_sessions():


    if not SESSION_FILE.exists():

        with open(
            SESSION_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                {},
                file
            )


        return {}



    with open(
        SESSION_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)




def save_sessions(data):


    with open(
        SESSION_FILE,
        "w",
        encoding="utf-8"
    ) as file:


        json.dump(
            data,
            file,
            indent=4
        )





def save_conversation(
        user,
        message,
        intent,
        response
):


    if LOG_FILE.exists():

        with open(
            LOG_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            logs = json.load(file)


    else:

        logs = []



    logs.append({

        "timestamp":
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "user":
        user,

        "message":
        message,

        "intent":
        intent,

        "response":
        response

    })



    with open(
        LOG_FILE,
        "w",
        encoding="utf-8"
    ) as file:


        json.dump(
            logs,
            file,
            indent=4
        )