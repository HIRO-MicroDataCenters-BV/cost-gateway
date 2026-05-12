from typing import Callable

import asyncio
import datetime
from unittest import IsolatedAsyncioTestCase


class AsyncTestFixture(IsolatedAsyncioTestCase):
    loop: asyncio.AbstractEventLoop
    terminated: asyncio.Event

    def setUp(self) -> None:
        super().setUp()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.terminated = asyncio.Event()

    def tearDown(self) -> None:
        super().tearDown()
        self.terminated.set()
        if self.loop and not self.loop.is_closed():
            self.loop.close()

    def wait_for_condition(self, seconds: int, conditionFunc: Callable[[], bool]) -> None:
        start = datetime.datetime.now()
        while start + datetime.timedelta(seconds=seconds) > datetime.datetime.now():
            if conditionFunc():
                return
            self.loop.run_until_complete(asyncio.sleep(0.1))
        raise AssertionError("time is up.")
