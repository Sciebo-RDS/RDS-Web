from flask import Flask
import uuid
import os
import json
from flask_socketio import SocketIO

development_mode = (os.getenv('DEV_FLASK_DEBUG', 'False') == 'True')

app = Flask(__name__,
            static_folder=os.getenv(
                "FLASK_STATIC_FOLDER", "/usr/share/nginx/html")
            )
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", uuid.uuid4().hex)

socketio = SocketIO(
    app, cors_allowed_origins=json.loads(os.getenv("FLASK_ORIGINS"))
)


clients = {}

# temporary user_store
user_store = {}

cache = {}
if os.getenv("DEV_FLASK_USE_JSON", "False") == "True":
    try:
        f = open("responses.json")
        cache = json.load(f)
    finally:
        f.close()


def store(key, iter):
    cache[key] = iter
    return iter
