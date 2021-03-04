
if __name__ == "__main__":
    from dotenv import load_dotenv
    from pathlib import Path
    env_path = Path('..') / '.env'
    load_dotenv(dotenv_path=env_path)
    
    from src.server import app, socketio, development_mode

    socketio.run(app, debug=development_mode, port=8080)
