from flask import Flask
import uuid
import os
import json
from flask_socketio import SocketIO
from flask_session import Session

from pathlib import Path
from dotenv import load_dotenv
env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

use_predefined_user = (os.getenv('DEV_USE_PREDEFINED_USER', 'False') == 'True')
use_embed_mode = (os.getenv('EMBED_MODE', 'False') == 'True')
use_proxy = (os.getenv('DEV_USE_PROXY', 'False') == 'True')
redirect_url = os.getenv("REDIRECTION_URL")


app = Flask(__name__,
            static_folder=os.getenv(
                "FLASK_STATIC_FOLDER", "/usr/share/nginx/html")
            )
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", uuid.uuid4().hex)
app.config['SESSION_TYPE'] = 'filesystem'
app.config["REMEMBER_COOKIE_HTTPONLY"] = False

Session(app)

print(os.getenv("FLASK_ORIGINS"))

socketio = SocketIO(
    app,
    cors_allowed_origins=json.loads(os.getenv("FLASK_ORIGINS")),
    manage_session=False
)


clients = {}

# temporary user_store
user_store = {}
