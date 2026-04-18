from app.core.config import get_settings

try:
    from celery import Celery
except ModuleNotFoundError:  # pragma: no cover - used only before dependencies are synced
    Celery = None  # type: ignore[assignment]


settings = get_settings()

if Celery is None:  # pragma: no cover
    celery_app = None
else:
    celery_app = Celery(
        "focuspulse",
        broker=settings.celery.broker_url,
        backend=settings.celery.result_backend,
    )
    celery_app.conf.update(
        task_default_queue=settings.celery.default_queue,
        task_always_eager=settings.celery.task_always_eager,
    )
