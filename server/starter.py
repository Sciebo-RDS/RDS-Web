from gevent import monkey
monkey.patch_all()

from src.server import app, socketio
import os
from pathlib import Path
from dotenv import load_dotenv


env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

if __name__ == "__main__":
    try:
        socketio.run(app,
                     debug=os.getenv("DEV_FLASK_DEBUG", "False") == "True",
                     port=5000
                     )
    finally:
        pass
