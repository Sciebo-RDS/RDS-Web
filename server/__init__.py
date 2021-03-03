from flask import Flask
import uuid
import os
from dotenv import load_dotenv
from pathlib import Path
env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", uuid.uuid4().hex)
