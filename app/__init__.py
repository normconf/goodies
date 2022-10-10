# app main -- setup logging

import os
from logging import NOTSET, Logger

import structlog


def am_i_on_ecs() -> bool:
    return os.getenv("ECS_CONTAINER_METADATA_URI_V4") is not None


def configure_logger() -> Logger:
    log_configuration = {
        "processors": [
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(),
            structlog.dev.ConsoleRenderer(),
        ],
        "wrapper_class": structlog.make_filtering_bound_logger(NOTSET),
        "context_class": dict,
        "logger_factory": structlog.PrintLoggerFactory(),
        "cache_logger_on_first_use": False,
    }

    if am_i_on_ecs():
        log_configuration["processors"] = [structlog.processors.JSONRenderer()]
    structlog.configure(**log_configuration)
    return structlog.get_logger()
