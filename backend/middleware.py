import logging
import logging.config
import json
import time
import uuid
from fastapi import Request

from config import settings

def setup_logging():
    """Configure structured logging for the application."""
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "structured": {
                "format": json.dumps({
                    "timestamp": "%(asctime)s",
                    "level": "%(levelname)s",
                    "message": "%(message)s",
                    "module": "%(name)s",
                    "request_id": "%(request_id)s",
                    "service": settings.service_name,
                    "environment": settings.node_env
                }).replace('"%(', '%(').replace(')s"', ')s')
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "structured",
                "stream": "ext://sys.stdout"
            }
        },
        "root": {
            "level": "INFO",
            "handlers": ["console"]
        }
    }

    logging.config.dictConfig(LOGGING_CONFIG)

async def add_request_id_middleware(request: Request, call_next):
    """
    Middleware to add request ID to all requests and responses.

    Adds structured logging with request correlation and performance metrics.
    """
    logger = logging.getLogger(__name__)

    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    # Add request_id to logging context
    old_factory = logging.getLogRecordFactory()
    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.request_id = getattr(request.state, 'request_id', 'unknown')
        return record
    logging.setLogRecordFactory(record_factory)

    start_time = time.time()

    # Log request start
    logger.info("Request started", extra={
        "method": request.method,
        "url": str(request.url),
        "user_agent": request.headers.get("user-agent", "")
    })

    response = await call_next(request)

    # Log request completion
    process_time = time.time() - start_time
    logger.info("Request completed", extra={
        "method": request.method,
        "url": str(request.url),
        "status_code": response.status_code,
        "process_time": round(process_time, 3)
    })

    # Add request ID to response headers
    response.headers["X-Request-ID"] = request_id

    # Restore original factory
    logging.setLogRecordFactory(old_factory)

    return response