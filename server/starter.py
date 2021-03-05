from dotenv import load_dotenv
from pathlib import Path
env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

from src.server import app, socketio, development_mode
from src.app import cache


if __name__ == "__main__":
    try:
        socketio.run(app, debug=development_mode, port=8080)
    finally:
        import json
        with open("responses.json", "x") as f:
            json.dump(cache, f)
