from __future__ import annotations

from typing import Any, ClassVar, Mapping, Sequence, get_type_hints

from pydantic import BaseModel
from pydantic.fields import FieldInfo

from .field import QueryField
from .query import Query


class BaseRecord(BaseModel):
    """
    Pydantic-backed base model with query support.

    - Data fields: standard Pydantic fields (can use alias for backend keys).
    - Query fields: available via `ClassName.q.<field>` (created from Pydantic
                    metadata).
    """

    # Populated at subclass creation time
    _query_fields: ClassVar[Mapping[str, QueryField] | None] = None
    # simple attribute container exposing QueryField per model field
    q: ClassVar[Any] = None

    # Example common field (optional):
    # id: str = PydField(..., alias="id")

    def to_backend(self) -> dict:
        """Dump to provider payload (uses field aliases)."""
        return self.model_dump(by_alias=True, exclude_unset=True, exclude_none=True)

    @classmethod
    def from_backend(cls, row: dict) -> "BaseRecord":
        """Hydrate from a provider dict (expects provider keys = aliases)."""
        return cls.model_validate(row)

    @classmethod
    def fields(cls) -> Sequence[QueryField]:
        """All query fields for this model."""
        return tuple(cls._query_fields.values())

    @classmethod
    def query(cls, session, *fields: QueryField) -> "Query":
        """
        Create a Query builder.

        If `fields` is empty → provider should decide default projection
        (or fetch all fields if supported).
        """
        use_fields = list(fields) if fields else None
        return Query(model=cls, session=session, fields=use_fields)

    @classmethod
    def _ensure_q(cls) -> None:
        """
        Ensure that this model class has its query interface (`q`) and field mapping
        (`_query_fields`) initialized.

        This method is responsible for building the `q` attribute — a container of
        `QueryField` instances matching each Pydantic model field — and storing them
        in `_query_fields` for later reuse.

        Initialization follows two strategies:

        1. **Compiled Pydantic path** – If the model has been compiled by Pydantic
           (i.e., `model_fields` is populated), those definitions are used directly.
        2. **Fallback path** – If the model has *not* been compiled yet, the method
           inspects the class `__annotations__` and retrieves any `FieldInfo`
           objects defined at class level to reconstruct the field metadata. This
           avoids depending on Pydantic's compilation timing, which can vary between
           environments (e.g., REPL vs. pytest).

        Each `QueryField` uses the Pydantic field's alias (if defined) as its
        `backend_key`, otherwise it falls back to the field's logical name.

        This method is idempotent: if `_query_fields` and `q` are already populated,
        it will return immediately without rebuilding.

        Raises:
            RuntimeError: If no fields can be derived from either the compiled
                Pydantic model or the class annotations/`FieldInfo` attributes.

        Side Effects:
            - Sets the `_query_fields` class variable to a mapping of field names
              to `QueryField` instances.
            - Creates and assigns a `q` attribute on the class, whose attributes
              mirror the model field names and point to their `QueryField` objects.
        """
        if cls._query_fields is not None and cls.q is not None:
            return

        pyd_fields = getattr(cls, "model_fields", {}) or {}
        if not pyd_fields:
            # Resolve annotations w/ postponed evaluation
            ann = get_type_hints(cls, include_extras=True) or {}
            derived: dict[str, FieldInfo] = {}
            for name in ann.keys():
                attr = getattr(cls, name, None)
                if isinstance(attr, FieldInfo):
                    derived[name] = attr
                else:
                    # Not a FieldInfo; still accept as a plain field (no alias)
                    # This lets simple annotated fields (no Field(...)) work too.
                    derived[name] = FieldInfo.from_annotation(ann[name])
            pyd_fields = derived  # shape: name -> FieldInfo

        if not pyd_fields:
            raise RuntimeError(
                f"{cls.__name__}: could not derive fields from Pydantic metadata "
                "(model_fields empty and no FieldInfo on class). "
                "Check your imports (use `from pydantic import Field`) and annotations."
            )

        qfields: dict[str, QueryField] = {}
        for name, finfo in pyd_fields.items():
            alias = finfo.alias or name
            qfields[name] = QueryField(name=name, backend_key=alias)
        cls._query_fields = qfields

        class _Q: ...

        q = _Q()
        for logical, qf in qfields.items():
            setattr(q, logical, qf)
        cls.q = q

    # --- Pydantic hook to build q/QueryFields ---
    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        # Build QueryField map from Pydantic model fields
        cls._ensure_q()
