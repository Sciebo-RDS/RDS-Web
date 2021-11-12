try:
    import eventlet
    eventlet.monkey_patch()
except ImportError:
    pass

from src.server import app, socketio, tracer_obj
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

if __name__ == "__main__":
    socketio.run(app,
                 debug=os.getenv("DEV_FLASK_DEBUG", "False") == "True",
                 host="0.0.0.0",
                 port=8080,
                 log_output=True
                 )

else:
    from flask_opentracing import FlaskTracing
    from src.TracingHandler import TracingHandler

    tracing = FlaskTracing(tracer_obj, True, app)

    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.handlers.append(TracingHandler(tracer_obj))
    app.logger.setLevel(gunicorn_logger.level)
