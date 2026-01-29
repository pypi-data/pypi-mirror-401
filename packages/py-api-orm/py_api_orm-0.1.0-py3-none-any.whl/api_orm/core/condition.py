from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

# Forward refs to avoid circular imports in type hints
# (used only for annotations to keep runtime clean)
if False:
    from .field import QueryField

Operator = Literal["eq", "ne"]  # Extend later


@dataclass(frozen=True)
class Condition:
    """A single filter condition produced by QueryField operators."""

    field: "QueryField"  # logical/alias-aware field
    op: Operator  # "eq", "ne", etc.
    value: Any  # right-hand side value

    def __repr__(self) -> str:  # nicer debug prints
        return f"Condition({self.field.name} {self.op} {self.value!r})"
