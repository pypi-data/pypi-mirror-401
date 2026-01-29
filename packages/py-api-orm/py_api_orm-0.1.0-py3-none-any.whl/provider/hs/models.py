from typing import Any

from pydantic import Field as PydField

from lib.api_orm.core.model import BaseRecord


class Company(BaseRecord):
    resource_name: str = PydField("COMPANIES")
    id: str | None = PydField(None, alias="hs_object_id")

    # Necessary fields taken from the field mapping data
    name: str | None = PydField(None, alias="name")
    street: str | None = PydField(None, alias="address")
    city: str | None = PydField(None, alias="city")
    country: str | None = PydField(None, alias="country")
    zip: str | None = PydField(None, alias="zip")
    vat_number: str | None = PydField(None, alias="vat_id")
    subscription_type: str | None = PydField(None, alias="subscription_status_")


class Contact(BaseRecord):
    resource_name: str = PydField("CONTACTS", alias="resource_name")
    id: str | None = PydField(None, alias="hs_object_id")

    # Necessary fields taken from the field mapping data
    name: str | None = PydField(None, alias="firstname")
    surname: str | None = PydField(None, alias="lastname")
    email: str | None = PydField(None, alias="email")
    phone: str | None = PydField(None, alias="phone")
    persona: str | None = PydField(None, alias="tatigkeitsfeld")
    gender: str | None = PydField(None, alias="sunify_gender")
    company: str | None = PydField(None, alias="company")
    street: str | None = PydField(None, alias="address")
    city: str | None = PydField(None, alias="city")
    country: str | None = PydField(None, alias="country")
    zip: str | None = PydField(None, alias="zip")
    smartstore_id: str | None = PydField(None, alias="smartstore_id")

    @classmethod
    def parse_from_mapping(cls, obj: dict[str, Any], mapping: dict[str, Any]):
        for external_name, internal_name in mapping.items():
            value = obj[external_name]
            setattr(cls, internal_name, value)
        cls.surname = obj["firstname"]
        return cls

    @classmethod
    def from_dataframe(cls, data) -> list["Contact"]:
        pass


class Deal(BaseRecord):
    resource_name: str = PydField("DEALS")
    id: str | None = PydField(None, alias="hs_object_id")

    # Necessary fields taken from the field mapping data
    name: str | None = PydField(None, alias="dealname")
    stage: str | None = PydField(None, alias="dealstage")
    request_id: str | None = PydField(None, alias="sunify_request_id")
    offer_id: str | None = PydField(None, alias="sunify_offer_id")
    offer_sum: str | None = PydField(None, alias="project_ammount")
    order_number: str | None = PydField(None, alias="sunify_order_number")
    offer_file_uri: str | None = PydField(None, alias="offer_uri")
    invoice_id: str | None = PydField(None, alias="invoice_id")
    invoice_sum: str | None = PydField(None, alias="actual_amount")
    invoice_number: str | None = PydField(None, alias="invoice_number")
    invoice_file_uri: str | None = PydField(None, alias="invoice_uri")
    construction_start: str | None = PydField(None, alias="construction_start_date")
    construction_end: str | None = PydField(None, alias="construction_end_date")
    project_type: str | None = PydField(None, alias="project_type")
    street: str | None = PydField(None, alias="project_street")
    city: str | None = PydField(None, alias="project_city")
    country: str | None = PydField(None, alias="project_country")
    zip: str | None = PydField(None, alias="project_zip")


class Lead(BaseRecord):
    resource_name: str = PydField("LEADS")
    id: str | None = PydField(None, alias="hs_object_id")

    # Necessary fields taken from the field mapping data
    request_id: str | None = PydField(None, alias="sunify_request_id")
    request_start_date: str | None = PydField(None, alias="request_start_date")
    request_end_date: str | None = PydField(None, alias="request_end_date")
    project_type: str | None = PydField(None, alias="project_type")
    street: str | None = PydField(None, alias="project_street")
    city: str | None = PydField(None, alias="project_city")
    country: str | None = PydField(None, alias="project_country")
    zip: str | None = PydField(None, alias="project_zip")
