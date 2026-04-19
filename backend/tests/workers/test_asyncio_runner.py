import asyncio

from app.workers import asyncio_runner


async def _current_loop_id() -> int:
    return id(asyncio.get_running_loop())


def test_worker_async_runner_reuses_one_event_loop() -> None:
    first_loop_id = asyncio_runner.run_async(_current_loop_id())
    second_loop_id = asyncio_runner.run_async(_current_loop_id())

    assert second_loop_id == first_loop_id
