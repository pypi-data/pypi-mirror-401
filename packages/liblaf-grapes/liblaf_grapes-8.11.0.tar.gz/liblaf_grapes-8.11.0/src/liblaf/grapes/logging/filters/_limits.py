import functools
import logging
import types
from collections.abc import Iterable, Sequence
from typing import Any

import attrs
import limits


@attrs.define
class LimitsFilter:
    limiter: limits.strategies.RateLimiter = attrs.field(
        factory=lambda: limits.strategies.FixedWindowRateLimiter(
            limits.storage.MemoryStorage()
        )
    )

    def filter(self, record: logging.LogRecord) -> bool:
        args: Any = getattr(record, "limits", None)
        if args is None:
            return True
        hit_args: LimitsHitArgs = _parse_args(args)
        if hit_args.item is None:
            return True
        return self.limiter.hit(
            hit_args.item, *hit_args.make_identifiers(record), cost=hit_args.cost
        )


@functools.singledispatch
def _parse_item(item: str | limits.RateLimitItem | None) -> limits.RateLimitItem | None:
    raise TypeError(item)


@_parse_item.register(types.NoneType)
def _(_item: None) -> None:
    return None


@_parse_item.register(str)
def _(item: str) -> limits.RateLimitItem:
    return limits.parse(item)


@_parse_item.register(limits.RateLimitItem)
def _(item: limits.RateLimitItem) -> limits.RateLimitItem:
    return item


@attrs.define
class LimitsHitArgs:
    item: limits.RateLimitItem | None = attrs.field(converter=_parse_item)
    namespace: Iterable[str] | None = attrs.field(default=None)
    identifiers: Iterable[str] = attrs.field(default=())
    cost: int = 1

    def make_identifiers(self, record: logging.LogRecord) -> Sequence[str]:
        namespace: Iterable[str] = (
            self._default_namespace(record)
            if self.namespace is None
            else self.namespace
        )
        return (*namespace, *self.identifiers)

    @staticmethod
    def _default_namespace(record: logging.LogRecord) -> Sequence[str]:
        return record.pathname, str(record.lineno), record.levelname


@functools.singledispatch
def _parse_args(args: Any) -> LimitsHitArgs:
    raise ValueError(args)


@_parse_args.register(str | limits.RateLimitItem)
def _(args: str | limits.RateLimitItem) -> LimitsHitArgs:
    return LimitsHitArgs(item=args)


@_parse_args.register(LimitsHitArgs)
def _(args: LimitsHitArgs) -> LimitsHitArgs:
    return args
