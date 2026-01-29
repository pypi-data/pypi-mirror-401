# Copyright 2023-2024, 2026 Dominik Sekotill <dom.sekotill@kodo.org.uk>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""
Asynchronous, multi-endpoint object delivery

Similarity to a single message queue or channel, a `Broadcast` asynchronously sends objects
(messages) to waiting tasks; however a `Broadcast` delivers to all waiting tasks that are
listening when the underlying lock is acquired.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import anyio.lowlevel


class Broadcast[T]:
	"""
	A reliable, blocking message queue for delivering to multiple listening tasks

	Listeners MUST acquire the lock (by using the `Broadcast` instance as a context manager)
	before calling `Broadcast.receive()` or it will fail.  Only messages sent while
	a listener is in the context are guaranteed to be delivered, so to avoid lost messages
	a listener should await all messages in a single lock context.

	i.e. If a listener is repeatedly awaiting messages in a loop, the loop should be inside
	the locked context or messages may be lost.

	Note that senders MUST NOT be in a locked context when sending.
	"""

	def __init__(self) -> None:
		super().__init__()
		self._condition = anyio.Condition()
		self._holds = 0
		self.obj: T | None = None
		self.exc: BaseException | type[BaseException] | None = None

	async def __aenter__(self) -> None:
		await self._condition.acquire()

	async def __aexit__(self, *_: object) -> None:
		self._condition.release()

	async def abort(self, exc: BaseException | type[BaseException]) -> None:
		"""
		Send a notification to all listeners to abort by raising an exception
		"""
		async with self._ready():
			assert self.exc is None and self.obj is None
			self.exc = exc
			self._condition.notify_all()
		await self._post()

	async def send(self, obj: T) -> None:
		"""
		Send a message object and block until all listeners have received it
		"""
		async with self._ready():
			assert self.exc is None and self.obj is None
			self.obj = obj
			self._condition.notify_all()
		await self._post()

	@asynccontextmanager
	async def _ready(self) -> AsyncIterator[None]:
		# Note: missing branch coverage in this function is probably due to race conditions
		# in tests/test_broadcast.py:BroadcastTests.test_send_multiple_senders; rerun tests
		# and see if the coverage changes.
		while 1:
			await anyio.lowlevel.checkpoint()
			async with self:
				if self.obj is not None or self.exc is not None:
					continue
				yield
				return

	async def _post(self) -> None:
		# Note: missing branch coverage in this function is probably due to race conditions
		# in tests/test_broadcast.py:BroadcastTests.test_send_multiple_listeners; rerun
		# tests and see if the coverage changes.

		# ensure listeners have opportunity to wait for locks
		await anyio.lowlevel.checkpoint()

		# Ensure all listeners have had a chance to lock and process self.obj
		while 1:
			async with self:
				assert self._holds >= 0, "there should never be a negative number of holds"
				if (
					self._holds
					or self._condition.statistics().lock_statistics.tasks_waiting
				):
					continue
				self.obj = self.exc = None
				break

	async def receive(self) -> T:
		"""
		Listen for a single message and return it once it arrives

		Note that the broadcast lock must be held when calling this method (see `Broadcast`).
		"""
		await self._condition.wait()
		if self.exc is not None:
			raise self.exc
		assert self.obj is not None
		return self.obj

	def process_message(self) -> _ProcessContext:
		"""
		Return an async context manager that is entered when a message is received

		The message sender is prevented from completing until the context exits.

		Normally `Broadcast.send()` returns once all listening tasks have received the
		message, but does not guarantee they have processed it. The returned context manager
		allows listeners to process messages before the sending coroutine returns.

		Note that the broadcast lock must be held when calling this method (see `Broadcast`).

		>>> async def process_message(broadcast: Broadcast[str], task_status: anyio.TaskStatus[None]) -> None:
		...     async with broadcast:  # Lock must be held to receive messages
		...        task_status.started()
		...        async with broadcast.process_message() as message:
		...            # Do any async operations with the message here
		...            await anyio.sleep(1)
		...            print(message)
		...
		>>> async def send_message(broadcast: Broadcast[str]) -> None:
		...     await broadcast.send("Hello world!")
		...     print("and goodbye.")
		...
		>>> @anyio.run
		... async def start_tasks() -> None:
		...     broadcast = Broadcast[str]()
		...     async with anyio.create_task_group() as tasks:
		...         await tasks.start(process_message, broadcast)
		...         await send_message(broadcast)
		...
		Hello world!
		and goodbye.
		"""
		return _ProcessContext(self)


class _ProcessContext[T]:
	def __init__(self, broadcast: Broadcast[T]) -> None:
		self.broadcast = broadcast

	async def __aenter__(self) -> T:
		msg = await self.broadcast.receive()
		self.broadcast._holds += 1  # noqa: SLF001
		return msg

	async def __aexit__(self, *_: object) -> None:
		self.broadcast._holds -= 1  # noqa: SLF001
