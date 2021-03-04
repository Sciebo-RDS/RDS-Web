from flask import Flask
import uuid
import os
import json
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", uuid.uuid4().hex)

socketio = SocketIO(
    app, cors_allowed_origins=json.loads(os.getenv("FLASK_ORIGINS"))
)
