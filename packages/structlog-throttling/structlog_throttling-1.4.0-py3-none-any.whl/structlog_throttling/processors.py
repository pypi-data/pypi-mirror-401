from __future__ import annotations

import collections.abc
import logging
import typing

from structlog import DropEvent
from structlog.typing import EventDict

from .throttlers import (
    CountThrottler,
    ThrottlerProtocol,
    TimeThrottler,
    TokenBucketThrottler,
    UniformThrottler,
    _default_calculate_tokens_per_key,
    _Hashable,
)

__all__ = [
    "CountThrottler",
    "LogThrottler",
    "LogTimeThrottler",
    "ThrottlerProtocol",
    "TimeThrottler",
    "TokenBucketThrottler",
    "UniformThrottler",
]


class LogThrottlerProtocol(typing.Protocol):
    key: tuple[str, ...]
    throttler: ThrottlerProtocol

    def __call__(self, _: logging.Logger, __: str, event_dict: EventDict) -> EventDict:
        try:
            key = tuple(event_dict[k] for k in self.key)
        except KeyError:
            return event_dict

        if self.throttler.is_throttled(key):
            raise DropEvent

        return event_dict


class LogThrottler(LogThrottlerProtocol):
    """Drop logs when throttled based on *throttler*.

    This should generally be close to the top of your processor chain so that a log that
    will ultimately be throttled is not processed further.

    Args:
        key: Unique key in the *event_dict* to determine if log should be throttled.
        throttler:
            A ``ThrottlerProtocol`` implementation to decide if *key should be
            throttled.
    """

    def __init__(
        self,
        key: str | collections.abc.Iterable[str],
        throttler: ThrottlerProtocol,
    ):
        self.key = (key,) if isinstance(key, str) else tuple(key)
        self.throttler = throttler


class LogTimeThrottler(LogThrottlerProtocol):
    """Drop logs when throttled based on time in between calls.

    This is a convenience class to initialize a ``LogThrottler`` with a
    ``TimeThrottler``.

    Args:
        key: Unique key in the *event_dict* to determine if log should be throttled.
        every_seconds: How long to throttle logs for, in seconds.
    """

    def __init__(
        self, key: str | collections.abc.Iterable[str], every_seconds: int | float
    ) -> None:
        self.key = (key,) if isinstance(key, str) else tuple(key)
        self.throttler = TimeThrottler(every_seconds)


class LogCountThrottler(LogThrottlerProtocol):
    """Drop logs when throttled based on the number of times *key* was in a log call.

    This is a convenience class to initialize a ``LogThrottler`` with a
    ``CountThrottler``.

    Args:
        key: Unique key in the *event_dict* to determine if log should be throttled.
        every_calls: Only allow logging every *every* times.
    """

    def __init__(self, key: str | collections.abc.Iterable[str], every: int) -> None:
        self.key = (key,) if isinstance(key, str) else tuple(key)
        self.throttler = CountThrottler(every)


class LogUniformThrottler(LogThrottlerProtocol):
    """Drop logs when throttled based on a uniform distribution.

    This is a convenience class to initialize a ``LogThrottler`` with a
    ``UniformThrottler``.

    Args:
        key: Unique key in the *event_dict* to determine if log should be throttled.
        rate:
            Log throttling rate. Represented as a number between 0 (never throttled) and
            1 (always throttle).
    """

    def __init__(
        self, key: str | collections.abc.Iterable[str], rate: float | int
    ) -> None:
        self.key = (key,) if isinstance(key, str) else tuple(key)
        self.throttler = UniformThrottler(rate)


class LogTokenBucketThrottler(LogThrottlerProtocol):
    """Drop logs when throttled based on a token bucket algorithm.

    This is a convenience class to initialize a ``LogThrottler`` with a
    ``TokenBucketThrottler``.

    Args:
        key: Unique key in the *event_dict* to determine if log should be throttled.
        max_tokens: Maximum tokens that a bucket can hold.
        replenish_seconds:
            Tokens are replenished in the bucket at a rate of 1 every
            *replenish_seconds*.
        calculate_tokens_per_key: Optionally provide a callable to determine how many
            tokens a given *key* should use up. By default, this is just 1.
    """

    def __init__(
        self,
        key: str | collections.abc.Iterable[str],
        max_tokens: int,
        replenish_seconds: int | float,
        calculate_tokens_per_key: typing.Callable[
            [_Hashable], int
        ] = _default_calculate_tokens_per_key,
    ) -> None:
        self.key = (key,) if isinstance(key, str) else tuple(key)
        self.throttler = TokenBucketThrottler(
            max_tokens, replenish_seconds, calculate_tokens_per_key
        )
