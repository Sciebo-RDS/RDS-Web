from flask import Flask
import uuid
import os

app = Flask(__name__, template_folder="../dist",
            static_folder="../dist", static_url_path="")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", uuid.uuid4().hex)
