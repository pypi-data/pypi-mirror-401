from typing import Iterable, Sequence

from hubspot.crm.companies import PublicObjectSearchRequest
from hubspot.crm.contacts import SimplePublicObject

import lib.provider.hs.client as hsclient
from lib.api_orm.core.condition import Condition
from lib.api_orm.core.field import QueryField
from lib.api_orm.core.model import BaseRecord
from lib.api_orm.core.session import BaseSession
from lib.provider.hs.helpers import ObjectType, normalize_key
from lib.provider.hs.models import Contact


class Session(BaseSession):

    def __init__(self):
        self._objects = []

    def add(self, record: BaseRecord) -> None:
        self._objects.append(record)

    def get_objects(self):
        copy = self._objects.copy()
        return copy

    def clear_objects(self):
        self._objects.clear()

    def commit(self) -> None:
        """
        Commits all the objects currently in the session to the client.
        Every object will be newly created, unless it has the "id" field,
        in which case it will get updated.
        """
        for obj in self._objects:
            properties = {}
            for field in obj.fields():
                if (
                    field.backend_key == "hs_object_id"
                    or field.backend_key == "q"
                    or field.backend_key == "resource_name"
                    or field.backend_key == "_query_fields"
                ):
                    continue
                value = getattr(obj, field.name)
                properties[field.backend_key] = value
            if getattr(obj, "id", None) is not None:
                hsclient.update_object(
                    ObjectType(obj.resource_name),
                    obj.id,
                    properties,
                )
            else:
                hsclient.create_object(ObjectType(obj.resource_name), properties, None)

    def fetch_one(
        self,
        model: type["BaseRecord"],
        fields: Sequence[QueryField] | None,
        conditions: Sequence[Condition],
    ) -> SimplePublicObject | None:

        search_object = self._evaluate_query(
            fields=fields, conditions=conditions, limit=1, order=None
        )
        res = hsclient.search(ObjectType(model.resource_name), search_object)
        return res.results[0] if len(res.results) > 0 else None

    def fetch_many(
        self,
        model: type["BaseRecord"],
        fields: Sequence[QueryField] | None,
        conditions: Sequence[Condition],
        limit: int | None = None,
        offset: int | None = None,
        order_by: Sequence[QueryField] | None = None,
    ) -> Iterable[dict]:

        search_object = self._evaluate_query(
            fields=fields, conditions=conditions, limit=limit, order=order_by
        )

        res = hsclient.search(ObjectType(model.resource_name), search_object).results
        start = offset if offset is not None else 0
        return res[start:]

    @staticmethod
    def _evaluate_query(
        fields: Sequence[QueryField] | None,
        conditions: Sequence[Condition] | None,
        order: Sequence[str] | None,
        limit: int | None,
    ) -> PublicObjectSearchRequest:
        search_object = PublicObjectSearchRequest()
        search_object = convert_query_fields(search_object, fields)
        search_object = convert_query_conditions(search_object, conditions)
        search_object = convert_query_order(search_object, order)
        search_object = convert_query_limits(search_object, limit)
        return search_object

    @staticmethod
    def _convert_external_service_body(external_body: dict) -> BaseRecord:
        for key, value in external_body.items():
            external_body[normalize_key(key)] = external_body.pop(key)
        res = Contact(**external_body)
        return res


def convert_query_fields(
    search_object: PublicObjectSearchRequest, fields: Sequence[QueryField] | None
) -> PublicObjectSearchRequest:

    properties = list()
    for field in fields:
        properties.append(field.backend_key)
    search_object.properties = properties
    return search_object


def convert_query_conditions(
    search_object: PublicObjectSearchRequest, conditions: Sequence[Condition] | None
) -> PublicObjectSearchRequest:

    filter_groups = list()
    for condition in conditions:
        filter_groups.append(
            {
                "filters": [
                    {
                        "propertyName": condition.field.backend_key,
                        "operator": condition.op.upper(),
                        "value": condition.value,
                    }
                ]
            }
        )
    search_object.filter_groups = filter_groups
    return search_object


def convert_query_limits(
    search_object: PublicObjectSearchRequest, limit: int | None
) -> PublicObjectSearchRequest:

    search_object.limit = limit
    return search_object


def convert_query_order(
    search_object: PublicObjectSearchRequest, order: list[str] | None
) -> PublicObjectSearchRequest:

    sorts = list()
    if order is not None:
        for order in order:
            property_name = order[1:]
            direction = order[:1]
            if direction == "-":
                direction = "DESCENDING"
            elif direction == "+":
                direction = "ASCENDING"

            sorts.append({"propertyName": property_name, "direction": direction})

    search_object.sorts = sorts
    return search_object
