from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics
import multiprocessing
from jaeger_client import Config as jConfig
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory
from flask_opentracing import FlaskTracing
from src.TracingHandler import TracingHandler

bind = "127.0.0.1:5000"
workers = multiprocessing.cpu_count() * 2 + 1
loglevel = "debug"
enable_stdio_inheritance = True
capture_output = True
errorlog = "-"
accesslog = "-"
worker_class = "eventlet"


def when_ready(server):
    GunicornPrometheusMetrics.start_http_server_when_ready(9999)


def child_exit(server, worker):
    GunicornPrometheusMetrics.mark_process_dead_on_child_exit(worker.pid)


def post_fork(server, worker):
    ### Tracing begin ###
    tracer_config = {
        "sampler": {"type": "const", "param": 1, },
        "local_agent": {
            "reporting_host": "jaeger-agent",
            "reporting_port": 5775,
        },
        "logging": True,
    }

    config = jConfig(
        config=tracer_config,
        service_name=f"RDSWebConnexionPlus",
        metrics_factory=PrometheusMetricsFactory(
            namespace=f"RDSWebConnexionPlus"
        ),
    )

    tracer_obj = config.initialize_tracer()
    tracing = FlaskTracing(tracer_obj, True, worker.app)
    worker.app.logger.handlers.extend(TracingHandler(tracer_obj))
