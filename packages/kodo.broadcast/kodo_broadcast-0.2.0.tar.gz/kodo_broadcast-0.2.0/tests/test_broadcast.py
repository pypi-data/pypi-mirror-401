"""
Tests for the kilter.service.sync.Broadcast class
"""

import pytest
import trio.lowlevel
import trio.testing

from kodo.broadcast import Broadcast


async def test_send_no_listeners() -> None:
	"""
	Check that sending a message with no listeners does not block
	"""
	broadcast = Broadcast[int]()

	with trio.move_on_after(2.0) as cancel_scope:
		await broadcast.send(1)

	assert not cancel_scope.cancelled_caught


async def test_send_one_listener() -> None:
	"""
	Check that sending a message to a single listener works
	"""
	broadcast = Broadcast[int]()
	messages = list[int]()

	async def listener() -> None:
		async with broadcast:
			messages.append(await broadcast.receive())

	async with trio.open_nursery() as task_group:
		task_group.start_soon(listener)
		await trio.testing.wait_all_tasks_blocked()

		await broadcast.send(1)
		await broadcast.send(2)

	assert messages == [1]


async def test_send_multiple_listeners() -> None:
	"""
	Check that sending a message to multiple listeners works
	"""
	NUM_LISTENERS = 10

	broadcast = Broadcast[int]()
	messages = list[int]()

	async def listener() -> None:
		async with broadcast:
			messages.append(await broadcast.receive())

	async with trio.open_nursery() as task_group:
		for _ in range(NUM_LISTENERS):
			task_group.start_soon(listener)
		await trio.testing.wait_all_tasks_blocked()

		await broadcast.send(1)
		await broadcast.send(2)

	assert messages == [1] * NUM_LISTENERS


async def test_send_multiple_senders() -> None:
	"""
	Check that sending from multiple tasks doesn't overwrite messages

	Note: this test relies on timing that is somewhat out of the test's control, so
	coverage *may* not be complete if an alt_sender task doesn't attempt to send at the
	same time as at least one other send in the main task.
	"""
	broadcast = Broadcast[int]()
	messages = set[int]()

	async def listener() -> None:
		async with broadcast:
			msg = 0
			while msg < 9:
				messages.add(msg := await broadcast.receive())

	async def alt_sender(msg: int) -> None:
		await broadcast.send(msg)

	async with trio.open_nursery() as task_group:
		task_group.start_soon(listener)
		await trio.testing.wait_all_tasks_blocked()

		await broadcast.send(1)
		task_group.start_soon(alt_sender, 2)
		await broadcast.send(3)
		await broadcast.send(4)
		await broadcast.send(5)
		task_group.start_soon(alt_sender, 6)
		await broadcast.send(7)
		await broadcast.send(8)
		await broadcast.send(9)

	assert messages == {1, 2, 3, 4, 5, 6, 7, 8, 9}


async def test_recieve_loop() -> None:
	"""
	Check that receiving multiple messages in a loop works
	"""
	broadcast = Broadcast[int]()
	messages = list[int]()

	async def listener() -> None:
		async with broadcast:
			msg = 0
			while msg < 4:
				msg = await broadcast.receive()
				messages.append(msg)

	async with trio.open_nursery() as task_group:
		task_group.start_soon(listener)
		task_group.start_soon(listener)
		await trio.testing.wait_all_tasks_blocked()

		for n in range(1, 10):  # Deliberately higher than the listeners go
			await broadcast.send(n)

	assert messages == [1, 1, 2, 2, 3, 3, 4, 4]


async def test_abort() -> None:
	"""
	Check that aborting with multiple listeners works
	"""
	broadcast = Broadcast[int]()

	async def listener() -> None:
		async with broadcast:
			with pytest.raises(ValueError):
				_ = await broadcast.receive()

	async with trio.open_nursery() as task_group:
		task_group.start_soon(listener)
		task_group.start_soon(listener)
		await trio.testing.wait_all_tasks_blocked()

		await broadcast.abort(ValueError)


async def test_process_message() -> None:
	"""
	Check that a sender is blocked while a process_message() context is entered
	"""
	broadcast = Broadcast[int]()
	messages = list[int]()

	async def listener() -> None:
		async with broadcast, broadcast.process_message() as message:
			await trio.sleep(0.4)
			messages.append(message)

	async with trio.open_nursery() as task_group:
		task_group.start_soon(listener)
		await trio.testing.wait_all_tasks_blocked()

		await broadcast.send(1)

		assert messages == [1]


# Not the best output when the test times-out, awaiting
# https://github.com/python-trio/pytest-trio/issues/53
@pytest.mark.timeout(1, method="thread")
async def test_process_message_deadlock(autojump_clock: object) -> None:
	"""
	Check that a process_message() context doesn't deadlock in a loop
	"""
	broadcast = Broadcast[int]()

	async def listener() -> None:
		async with broadcast:
			for _ in range(2):
				async with broadcast.process_message() as _:
					await trio.lowlevel.checkpoint()

	async with trio.open_nursery() as task_group:
		task_group.start_soon(listener)
		await trio.testing.wait_all_tasks_blocked()

		await broadcast.send(1)
		await broadcast.send(1)
