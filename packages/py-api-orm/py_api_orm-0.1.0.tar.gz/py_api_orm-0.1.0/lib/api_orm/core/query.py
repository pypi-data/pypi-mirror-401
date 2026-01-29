from __future__ import annotations

from typing import Iterable, Sequence

from .condition import Condition
from .field import QueryField

# Forward refs to avoid circular imports in type hints
# (used only for annotations to keep runtime clean)
if False:
    from .model import BaseRecord


class Query:
    """Fluent, provider-agnostic query builder."""

    __slots__ = (
        "model",
        "session",
        "_fields",
        "_conditions",
        "_limit",
        "_offset",
        "_order_by",
        "_raw_data",
    )

    def __init__(
        self,
        model: type["BaseRecord"],
        session,
        fields: Sequence[QueryField] | None = None,
    ):
        self.model = model
        self.session = session
        self._fields = list(fields) if fields else None
        self._conditions: list[Condition] = []
        self._limit: int | None = None
        self._offset: int | None = None
        self._order_by: list[QueryField] | None = None
        self._raw_data: dict | list[dict] | None = None

    @property
    def raw_data(self) -> dict:
        return self._raw_data

    @property
    def get_fields(self) -> list[QueryField] | None:
        return self._fields

    @property
    def get_conditions(self) -> list[Condition] | None:
        return self._conditions

    @property
    def get_limit(self) -> int | None:
        return self._limit

    @property
    def get_order_by(self) -> list[QueryField] | None:
        return self._order_by

    # Builders
    def where(self, *conditions: Condition) -> "Query":
        self._conditions.extend(conditions)
        return self

    def limit(self, n: int) -> "Query":
        self._limit = n
        return self

    def offset(self, n: int) -> "Query":
        self._offset = n
        return self

    def order_by(self, *fields: QueryField) -> "Query":
        self._order_by = list(fields) if fields else None
        return self

    # Terminals
    def one_or_none(self) -> BaseRecord | None:
        self._raw_data = self.session.fetch_one(
            model=self.model,
            fields=self._fields,
            conditions=self._conditions,
        )
        is_non_null_dict = isinstance(self._raw_data, dict) and len(self._raw_data) >= 0
        if is_non_null_dict:
            return self.model.from_backend(self._raw_data)
        if isinstance(self._raw_data, list) and len(self._raw_data) == 1:
            return self.model.from_backend(self._raw_data[0])
        return None

    def scalars(self) -> Iterable["BaseRecord"]:
        self._raw_data = self.session.fetch_many(
            model=self.model,
            fields=self._fields,
            conditions=self._conditions,
            limit=self._limit,
            offset=self._offset,
            order_by=self._order_by,
        )
        for row in self._raw_data:
            yield self.model.from_backend(row)
