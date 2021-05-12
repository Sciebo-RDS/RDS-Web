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
redirect_url = os.getenv("REDIRECT_URL")
authorize_url = os.getenv("AUTHORIZE_URL")

redirect_url = "{}?response_type=token&client_id={}&redirect_uri={}".format(
    authorize_url,
    os.getenv("OWNCLOUD_OAUTH_CLIENT_ID"),
    redirect_url
)


app = Flask(__name__,
            static_folder=os.getenv(
                "FLASK_STATIC_FOLDER", "/usr/share/nginx/html")
            )
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", uuid.uuid4().hex)
app.config['SESSION_TYPE'] = 'filesystem'
app.config["REMEMBER_COOKIE_HTTPONLY"] = False

Session(app)

print(os.getenv("FLASK_ORIGINS"))
path = os.getenv("SOCKETIO_PATH", "socket.io")

if(path.startswith("/")):
    path = path.replace("/", "", 1)

socketio = SocketIO(
    app,
    cors_allowed_origins=json.loads(os.getenv("FLASK_ORIGINS")),
    manage_session=False,
    path=path
)


clients = {}

# temporary user_store
user_store = {}
