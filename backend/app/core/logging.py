import logging
from collections.abc import Mapping
from typing import Any


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def log_with_request_id(
    logger: logging.Logger,
    level: int,
    message: str,
    *,
    request_id: str | None = None,
    extra: Mapping[str, Any] | None = None,
) -> None:
    payload = dict(extra or {})
    if request_id:
        payload["request_id"] = request_id
    logger.log(level, message, extra={"focuspulse": payload})
