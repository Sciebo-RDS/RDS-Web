try:
    from gevent import monkey
    monkey.patch_all()
except ImportError:
    pass

from src.server import app, socketio
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)

env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

if __name__ == "__main__":
    socketio.run(app,
                 debug=os.getenv("DEV_FLASK_DEBUG", "False") == "True",
                 host="0.0.0.0",
                 port=8080,
                 log_output=True
                 )
