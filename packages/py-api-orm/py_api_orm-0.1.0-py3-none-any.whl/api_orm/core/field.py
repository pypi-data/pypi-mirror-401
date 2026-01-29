from __future__ import annotations

from typing import Any

# Forward refs to avoid circular imports in type hints
# (used only for annotations to keep runtime clean)
if False:  # pragma: no cover
    from .condition import Condition  # noqa: F401


class QueryField:
    """
    Declarative query field (class-level expression builder).

    - `name` is the logical model field name (e.g., "email").
    - `backend_key` is the provider's field key (e.g., "hs_email") when it differs.
    """

    __slots__ = ("name", "backend_key")

    def __init__(self, name: str, *, backend_key: str | None = None):
        self.name = name
        self.backend_key = backend_key

    # MVP operators
    def __eq__(self, other: Any) -> "Condition":
        from .condition import Condition

        return Condition(field=self, op="eq", value=other)

    def __ne__(self, other: Any) -> "Condition":
        from .condition import Condition

        return Condition(field=self, op="ne", value=other)

    # Extend later: in_(), contains(), gt/lt, like(), etc.

    def __repr__(self) -> str:
        k = f", backend_key={self.backend_key!r}" if self.backend_key else ""
        return f"QueryField(name={self.name!r}{k})"
