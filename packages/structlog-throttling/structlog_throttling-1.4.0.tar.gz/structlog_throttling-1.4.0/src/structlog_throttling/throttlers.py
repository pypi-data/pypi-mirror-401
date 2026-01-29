from __future__ import annotations

import collections
import random
import time
import typing
import weakref


class _Hashable(typing.Protocol):
    def __hash__(self) -> int: ...


class ThrottlerProtocol(typing.Protocol):
    """Protocol for all throttlers."""

    def is_throttled(self, key: _Hashable) -> bool: ...


class _Link:
    """A link in a doubly-linked list"""

    __slots__ = "at", "previous", "__weakref__"
    previous: "_Link" | None
    at: float | None


class TimeThrottler:
    """A throttler for time-based throttling.

    The intuition is that if we determine that a particular key is no longer throttled,
    then it follows that any key that came before it (i.e. any key that was throttled
    with an earlier timestamp) is also no longer throttled. Thus it is possible to save
    memory by clearing multiple keys simultaneously.

    This is achieved by maintaining two data structures:
    * A linked list of ``_Link``.
    * A ``weakref.WeakValueDictionary`` mapping keys to links in the list.

    In each ``_Link`` of the doubly-linked list we store:
    * The timestamp observed when a ``key`` is throttled.
    * A strong reference to the ``previous`` ``_Link``, which will contain the
        registered timestamp for the ``key`` that was just previously throttled.

    The idea is that there is only one strong reference to each link: In the link that
    comes next in the list. This allows preserving memory by dropping multiple keys from
    the list simultaneously by dropping a single link in the list. By dropping a single
    link, we will drop the only strong reference to the previous link, thus it will also
    be garbage collected, and this will subsequently drop the only reference to the
    previous link of the previous link, which will also be garbage collected, and so on.

    This design was inspired by ``collections.OrderedDict``.
    """

    def __init__(self, every_seconds: int | float) -> None:
        self.every = every_seconds

        self._last: _Link | None = None
        self._indexes: weakref.WeakValueDictionary[_Hashable, _Link] = (
            weakref.WeakValueDictionary()
        )

    def is_throttled(self, key: _Hashable) -> bool:
        """Determine whether *key* is throttled.

        Examples:
            >>> tt = TimeThrottler(every_seconds=1)
            >>> tt.is_throttled("event")
            False
            >>> tt.is_throttled("event")
            True
            >>> tt.is_throttled("another-event")
            False
            >>> tt.is_throttled("another-event")
            True
            >>> time.sleep(1)
            >>> tt.is_throttled("event")
            False
            >>> tt.is_throttled("another-event")
            False
        """
        now = time.monotonic()

        if key not in self._indexes:
            new = _Link()
            new.at = now
            # Stores a weak reference
            self._indexes[key] = new

            if self._last:
                # 'previous' is a strong reference
                new.previous = self._last

            self._last = new

            return False

        link = self._indexes[key]
        if link.at and (now - link.at) >= self.every:
            if self._last == link:
                link.at = now
                return False

            if hasattr(link, "previous"):
                del link.previous
            link.previous = self._last
            self._last = link

            return False

        return True


class CountThrottler:
    """A throttler based on the count of times a key was seen."""

    def __init__(self, every: int) -> None:
        self.every = every

        self._counts: dict[_Hashable, int] = {}

    def is_throttled(self, key: _Hashable) -> bool:
        """Determine whether *key* is throttled.

        Examples:
            >>> ct = CountThrottler(every=2)
            >>> ct.is_throttled("event")
            False
            >>> ct.is_throttled("event")
            True
            >>> ct.is_throttled("event")
            False
        """
        if key not in self._counts:
            self._counts[key] = self.every

        current = self._counts[key]
        if current % self.every == 0:
            should_throttle = False
        else:
            should_throttle = True

        if current - 1 == 0:
            del self._counts[key]
        else:
            self._counts[key] = current - 1

        return should_throttle


class UniformThrottler:
    """A throttler based on a uniform distribution."""

    def __init__(
        self,
        rate: float | int,
    ) -> None:
        if not 0 <= rate <= 1:
            raise ValueError("'rate' must be between 0 and 1")

        self.rate = rate

    def is_throttled(self, key: _Hashable) -> bool:
        """Determine whether any *key* is throttled.

        Each call is independent, meaning that *key* is effectively ignored.
        """
        return random.uniform(0, 1) >= self.rate


Bucket = collections.namedtuple("Bucket", ("tokens", "last_filled"))


def _default_calculate_tokens_per_key(key: _Hashable):
    """By default each key uses up one token."""
    return 1


class TokenBucketThrottler:
    """A throttler using a token bucket algorithm.

    For each event *key*, initialize a bucket with ``self.max_tokens``. If there are
    enough tokens in the bucket, then the *key* is not throttled, otherwise then the
    *key* is throttled.

    Tokens are added to the bucket at a rate of 1 every ``self.replenish_seconds``.

    The tokens consumed by a particular *key* are determined by the callable
    ``self.calculate_tokens_per_key``, which by default is 1.
    """

    def __init__(
        self,
        max_tokens: int,
        replenish_seconds: int | float,
        calculate_tokens_per_key: typing.Callable[
            [_Hashable], int
        ] = _default_calculate_tokens_per_key,
    ) -> None:
        if not max_tokens >= 1:
            raise ValueError("'max_tokens' must be at least 1")

        if not replenish_seconds > 0:
            raise ValueError("'replentish_seconds' must be more than 0")

        self.max_tokens = max_tokens
        self.replenish_seconds = replenish_seconds
        self.calculate_tokens_per_key = calculate_tokens_per_key
        self._buckets = {}

    def is_throttled(self, key: _Hashable) -> bool:
        """Determine whether any *key* is throttled.

        Examples:
            >>> tokens_per_key = lambda key: 1 if key == "event" else 2
            >>> tbt = TokenBucketThrottler(max_tokens=2, replenish_seconds=1, calculate_tokens_per_key=tokens_per_key)
            >>> tbt.is_throttled("event")
            False
            >>> tbt.is_throttled("event")
            False
            >>> tbt.is_throttled("event")
            True
            >>> tbt.is_throttled("another-event")
            False
            >>> tbt.is_throttled("another-event")
            True
            >>> time.sleep(1)
            >>> tbt.is_throttled("event")
            False
            >>> tbt.is_throttled("another-event")
            True
            >>> time.sleep(1)
            >>> tbt.is_throttled("another-event")
            False
        """
        now = time.monotonic()

        if key not in self._buckets:
            self._buckets[key] = Bucket(self.max_tokens, now)

        bucket = self._buckets.pop(key)
        replenished_tokens = min(
            bucket.tokens + (now - bucket.last_filled) // self.replenish_seconds,
            self.max_tokens,
        )

        key_tokens = self.calculate_tokens_per_key(key)
        should_throttle = True

        if replenished_tokens >= key_tokens:
            replenished_tokens -= key_tokens
            should_throttle = False

        self._buckets[key] = Bucket(replenished_tokens, now)

        return should_throttle
