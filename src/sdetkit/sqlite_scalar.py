"""SQLite scalar-function registration utilities.

This module provides signature-aware registration helpers around
``sqlite3.Connection.create_function``.
"""

from __future__ import annotations

import functools
import inspect
import sqlite3
from collections.abc import Callable
from typing import Any
from weakref import WeakKeyDictionary

_ArityMap = dict[str, set[int]]
_ConnectionState = WeakKeyDictionary[sqlite3.Connection, _ArityMap]

# Tracks arities registered through this module so replace/keep semantics can be
# applied per-arity without clobbering other registrations.
_REGISTERED_ARITIES: _ConnectionState = WeakKeyDictionary()


class ScalarFunctionRegistrationError(ValueError):
    """Raised when a callable cannot be mapped to SQLite positional arities."""


def register_scalar_function(
    connection: sqlite3.Connection,
    func: Callable[..., Any] | None = None,
    *,
    name: str | None = None,
    num_args: int | None = None,
    replace: bool = False,
    deterministic: bool = False,
) -> Callable[..., Any]:
    """Register a scalar SQLite function using direct-call or decorator style.

    Supports both forms:

    - ``register_scalar_function(conn, my_func, ...)``
    - ``@register_scalar_function(conn, ...)``

    The returned value is always the original callable.
    """

    if func is None:

        def decorator(inner: Callable[..., Any]) -> Callable[..., Any]:
            register_scalar_function(
                connection,
                inner,
                name=name,
                num_args=num_args,
                replace=replace,
                deterministic=deterministic,
            )
            return inner

        return decorator

    resolved_name = name or _default_function_name(func)
    arities = _resolve_arities(func, num_args=num_args)
    _register_with_replace_semantics(
        connection,
        resolved_name,
        func,
        arities,
        replace=replace,
        deterministic=deterministic,
    )
    return func


def _default_function_name(func: Callable[..., Any]) -> str:
    base, _, _ = _unwrap_partial(func)
    if inspect.isclass(base):
        return base.__name__
    return getattr(base, "__name__", type(base).__name__)


def _resolve_arities(func: Callable[..., Any], *, num_args: int | None) -> set[int]:
    if num_args is not None:
        if num_args < -1:
            msg = "num_args must be -1 or a non-negative integer"
            raise ScalarFunctionRegistrationError(msg)
        return {num_args}

    base_callable, bound_args, bound_kwargs = _unwrap_partial(func)
    signature = inspect.signature(base_callable)

    required_positional = 0
    optional_positional = 0
    has_varargs = False

    consumed_positionals = 0
    bound_keyword_names = set(bound_kwargs)

    for parameter in signature.parameters.values():
        kind = parameter.kind

        if kind is inspect.Parameter.VAR_POSITIONAL:
            has_varargs = True
            continue

        if kind is inspect.Parameter.VAR_KEYWORD:
            continue

        if kind is inspect.Parameter.KEYWORD_ONLY:
            if parameter.name in bound_keyword_names:
                continue
            if parameter.default is inspect.Parameter.empty:
                msg = (
                    f"required keyword-only parameter '{parameter.name}' must be "
                    "bound before SQLite registration"
                )
                raise ScalarFunctionRegistrationError(msg)
            # Optional keyword-only parameters never affect positional arities.
            continue

        slot_filled = False
        if consumed_positionals < len(bound_args):
            consumed_positionals += 1
            slot_filled = True
        elif parameter.name in bound_keyword_names:
            slot_filled = True

        if slot_filled:
            continue

        if parameter.default is inspect.Parameter.empty:
            required_positional += 1
        else:
            optional_positional += 1

    if consumed_positionals < len(bound_args):
        msg = "too many positional arguments were bound for callable signature"
        raise ScalarFunctionRegistrationError(msg)

    if has_varargs:
        return {-1}

    max_positional = required_positional + optional_positional
    return set(range(required_positional, max_positional + 1))


def _unwrap_partial(
    func: Callable[..., Any],
) -> tuple[Callable[..., Any], tuple[Any, ...], dict[str, Any]]:
    bound_args: list[Any] = []
    bound_kwargs: dict[str, Any] = {}

    current: Any = func
    while isinstance(current, functools.partial):
        bound_args = [*current.args, *bound_args]
        if current.keywords:
            bound_kwargs = {**current.keywords, **bound_kwargs}
        current = current.func

    if not callable(current):
        msg = "registered object must be callable"
        raise ScalarFunctionRegistrationError(msg)

    return current, tuple(bound_args), bound_kwargs


def _register_with_replace_semantics(
    connection: sqlite3.Connection,
    name: str,
    func: Callable[..., Any],
    arities: set[int],
    *,
    replace: bool,
    deterministic: bool,
) -> None:
    tracked = _REGISTERED_ARITIES.setdefault(connection, {})
    existing = tracked.setdefault(name, set())

    fixed_arities = {arity for arity in arities if arity >= 0}
    has_varargs = -1 in arities

    if not replace:
        fixed_to_register = fixed_arities - existing
        varargs_to_register = has_varargs and -1 not in existing
    else:
        fixed_to_register = fixed_arities
        # replace=True for fixed arities must preserve any varargs overload.
        varargs_to_register = has_varargs and -1 not in existing

    for arity in sorted(fixed_to_register):
        connection.create_function(name, arity, func, deterministic=deterministic)
        existing.add(arity)

    if varargs_to_register:
        connection.create_function(name, -1, func, deterministic=deterministic)
        existing.add(-1)
