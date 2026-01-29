"""
Collection of classes extending the hubspot provided classes for easier interaction
with the API
"""

from enum import Enum

from hubspot import HubSpot
from hubspot.crm.association_type import AssociationType as HsAssociationType
from hubspot.crm.objects import ApiException
from hubspot.discovery.crm.contacts.discovery import Discovery
from provider.hs.models import Contact

from lib.api_orm.core.model import BaseModel
from lib.provider.hs import exceptions


class AssociationType(HsAssociationType):
    """
    Extending the Hubspot Association Types from the package with new types not included
    in the package
    """

    LEAD_TO_PRIMARY_CONTACT = 578
    LEAD_TO_CONTACT = 608
    LEAD_TO_COMPANY = 610
    LEAD_TO_CALL = 596
    LEAD_TO_EMAIL = 598
    LEAD_TO_MEETING = 600
    LEAD_TO_NOTE = 854
    LEAD_TO_TASK = 646
    LEAD_TO_COMMUNICATION = 602
    LEAD_TO_DEAL = 583


class AssociationCategory:
    HUBSPOT_DEFINED = "HUBSPOT_DEFINED"
    USER_DEFINED = "USER_DEFINED"


class ObjectType(str, Enum):
    CONTACTS = "CONTACTS"
    COMPANIES = "COMPANIES"
    DEALS = "DEALS"
    LEADS = "LEADS"


def get_api_interface_by_object_name(
    client: HubSpot, object_type: ObjectType
) -> Discovery:
    if object_type == ObjectType.LEADS:
        return client.crm.objects.leads
    return getattr(client.crm, object_type.value.lower())


def map_hubspot_exception(exc: ApiException) -> exceptions.HsClientError:
    status = exc.status
    body = exc.body or ""
    headers = exc.headers or {}

    if status == 404:
        return exceptions.ObjectNotFoundError("Object not found.")
    if status == 400:
        return exceptions.InvalidRequestError(body)
    if status == 401:
        return exceptions.AuthenticationError("Invalid or missing token.")
    if status == 403:
        return exceptions.PermissionDeniedError("Access denied.")
    if status == 409:
        return exceptions.NonUniqueObjectError("Duplicate object.")
    if status == 429:
        retry_after = int(headers.get("Retry-After", "0"))
        return exceptions.RateLimitExceededError(
            "Rate limit exceeded.", retry_after=retry_after
        )
    if 500 <= status < 600:
        return exceptions.ServerError("HubSpot server error.")

    # fallback
    return exceptions.HsClientError(f"Unexpected API error: {status}: {body}")


def normalize_key(key: str) -> str:
    """
    Takes a list of keys as argument and normalizes them
    to lowercase and split by underscores.
    """
    normalized_key = ""
    words = []
    for word in key.split(" "):
        words.append(word.lower())
    normalized_key += words[0]
    if len(words) > 1:
        for word in words[1:]:
            normalized_key += "_" + word
    return normalized_key


HUBSPOT_FIELDS = {
    "hs_object_id": ["id", "object_id"],
    "email": ["email", "email_address", "mail", "mail_address"],
    "firstname": ["firstname", "first_name", "name"],
    "lastname": ["lastname", "last_name", "surname"],
}


def convert_external_object(obj: dict) -> BaseModel:
    """
    Conversion from an external object to a categorized BaseModel object.
    Expects a dict with the properties of the object.
    """
    for key, value in obj.items():
        obj[normalize_key(key)] = obj.pop(key)
    for key in obj.keys():
        if key == "resource_name" or key == "resource_type":
            # ToDo: Map possibly random resource names to the hubspot names
            pass

    return Contact()
    pass
