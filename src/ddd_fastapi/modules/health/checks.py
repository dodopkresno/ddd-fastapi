from collections.abc import Awaitable, Callable

ReadinessCheck = Callable[[], Awaitable[bool]]
