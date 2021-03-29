from src.server import app, socketio, development_mode
from pathlib import Path
import os

from dotenv import load_dotenv
env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

print(os.getenv("FLASK_ORIGINS"))


if __name__ == "__main__":
    try:
        socketio.run(app, debug=development_mode, port=8080)
    finally:
        pass
