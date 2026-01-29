from __future__ import annotations

from typing import Iterable, Protocol, Sequence

from lib.api_orm.core.condition import Condition
from lib.api_orm.core.field import QueryField

# Forward refs to avoid circular imports in type hints
# (used only for annotations to keep runtime clean)
if False:
    from .model import BaseRecord


class BaseSession(Protocol):
    """
    Provider adapter API the core uses.
    Implement this per provider (HubSpot, Salesforce, custom REST, ...).
    """

    def add(self, record: BaseRecord) -> None:
        """
        Add a record to the session.
        """
        ...

    def commit(self) -> None:
        """
        Writes all the records in the session to the api.
        """
        ...

    def fetch_one(
        self,
        model: type["BaseRecord"],
        fields: Sequence[QueryField] | None,
        conditions: Sequence[Condition],
    ) -> dict | None:
        """
        Return a single backend row (as dict) or None.
        Must raise provider-mapped exceptions (converted to core ones in the provider).
        """
        ...

    def fetch_many(
        self,
        model: type["BaseRecord"],
        fields: Sequence[QueryField] | None,
        conditions: Sequence[Condition],
        *,
        limit: int | None = None,
        offset: int | None = None,
        order_by: Sequence[QueryField] | None = None,
    ) -> Iterable[dict]:
        """Return an iterable of backend rows (each a dict)."""
        ...
