import logging
import os
from typing import Any, Sequence

from dotenv import load_dotenv
from hubspot import HubSpot
from hubspot.crm.contacts import (
    CollectionResponseWithTotalSimplePublicObjectForwardPaging,
)
from hubspot.crm.objects import (
    PublicObjectSearchRequest,
    SimplePublicObjectInput,
    SimplePublicObjectInputForCreate,
    SimplePublicObjectWithAssociations,
)
from hubspot.crm.objects.exceptions import ApiException

from lib.provider.hs.exceptions import InvalidRequestError, ObjectNotFoundError
from lib.provider.hs.helpers import (
    ObjectType,
    get_api_interface_by_object_name,
    map_hubspot_exception,
)

logger = logging.getLogger(__name__)

_client: HubSpot = None


def get_client() -> HubSpot:
    """
    Lazily initialize and return the HubSpot client singleton.

    Returns:
        HubSpot: An authenticated HubSpot API client instance.

    Raises:
        RuntimeError: If the HUBSPOT_TOKEN environment variable is not set.
    """
    global _client
    if _client is None:
        load_dotenv()
        token = os.getenv("HUBSPOT_TOKEN")
        if not token:
            raise RuntimeError("HUBSPOT_TOKEN environment variable is not set.")
        _client = HubSpot(access_token=token)
    return _client


def _reset_client_for_testing() -> None:
    """
    Reset the HubSpot client singleton instance.

    For use in unit tests to ensure isolated client state.
    """
    global _client
    _client = None


def get_by_id(
    object_type: ObjectType, id_: str | int, properties: list[str] | None = None
) -> SimplePublicObjectWithAssociations | None:
    """
    Retrieve a single object by its HubSpot ID.

    Args:
        object_type: The type of object ("contact", "company", "deal", "lead").
        id_: The unique HubSpot object ID.
        properties: Optional list of properties to return.

    Returns:
        The object data as a dictionary.
    """

    if isinstance(id_, int):
        id_ = str(id_)

    if not isinstance(id_, str) or not id_.isdigit():
        raise InvalidRequestError(f"Invalid object ID: {id_!r}")

    try:
        api = get_api_interface_by_object_name(_client, object_type)
        logger.debug(
            f"Retrieving {object_type.value.capitalize()} "
            f"object by id={id_!r} with optional "
            f"properties={properties!r}"
        )
        obj = api.basic_api.get_by_id(id_, properties=properties)
        logger.info(f"Found {object_type.value.capitalize()} object: id={id_!r}")
        return obj
    except ApiException as exc:
        err = map_hubspot_exception(exc)

        if isinstance(err, ObjectNotFoundError):
            logger.warning(
                f"{object_type.value.capitalize()} object not found: id={id_}"
            )
            return None

        logger.error(
            f"Failed to get {object_type.value.capitalize()} with id={id_}: {err}",
            exc_info=True,
        )
        raise err


def get_all(
    object_type: ObjectType, properties: Sequence[str] | None = None
) -> list[SimplePublicObjectWithAssociations] | None:
    """
    Retrieve all objects of a given type.

    Args:
        object_type: The object type to fetch.
        properties: Optional properties to include in the returned objects

    Returns:
        A list of objects.
    """

    try:
        api = get_api_interface_by_object_name(_client, object_type)
        logger.debug(
            f"Retrieving all {object_type.value.capitalize()} "
            f"objects with optional properties={properties!r}"
        )
        obj = api.basic_api.get_page(properties=properties)
        logger.info(f"Retrieved all {object_type.value.capitalize()} objects")
        return obj
    except ApiException as exc:
        err = map_hubspot_exception(exc)

        if isinstance(err, ObjectNotFoundError):
            # logger.warning(f"object_type.value.capitalize()
            # objects not found during get_all")
            return None

        logger.error(
            f"Failed to get all {object_type.value.capitalize()}: {err}",
            exc_info=True,
        )
        raise err


def search(
    object_type: ObjectType, search_object: PublicObjectSearchRequest
) -> CollectionResponseWithTotalSimplePublicObjectForwardPaging | None:
    """
    Search for one or multiple objects by the SearchRequest Object.
     Returns None if none found.

    Args:
        object_type: The type of object to search.
        search_object: The SearchRequest object containing the search query.

    Returns:
        The search result as a dictionary or None.
    """

    try:
        api = get_api_interface_by_object_name(_client, object_type)
        obj = api.search_api.do_search(search_object)
        return obj

    except ApiException as exc:
        err = map_hubspot_exception(exc)

        if isinstance(err, ObjectNotFoundError):
            return None

        logger.error(
            f"Failed to get {object_type.value.capitalize()} "
            f"for property="
            f"{search_object.filter_groups[0]["filters"]["property_name"]}"
            f" with specified value: {err}",
            exc_info=True,
        )
        raise err


def update_object(
    object_type: ObjectType, id_: str, properties: dict[str, Any]
) -> dict | None:
    """
    Update an existing HubSpot object with new property values.

    Args:
        object_type: The type of object to update.
        id_: The object ID.
        properties: A dictionary of field values to update.

    Returns:
        The updated object.
    """

    if isinstance(id_, int):
        id_ = str(id_)

    if not isinstance(id_, str) or not id_.isdigit():
        raise InvalidRequestError(f"Invalid object ID: {id_!r}")

    try:
        api = get_api_interface_by_object_name(_client, object_type)
        logger.debug(
            f"Updating {object_type.value.capitalize()}"
            f" object by id={id_!r} with properties={properties!r}"
        )
        obj = api.basic_api.update(id_, SimplePublicObjectInput(properties=properties))
        logger.info(f"Updated {object_type.value.capitalize()} object: id={id_!r}")
        return obj
    except ApiException as exc:
        err = map_hubspot_exception(exc)

        if isinstance(err, ObjectNotFoundError):
            logger.warning(
                f"{object_type.value.capitalize()} "
                f"object not found during update: id={id_}"
            )
            return None

        logger.error(
            f"Failed to update {object_type.value.capitalize()} with id={id}: {err}",
            exc_info=True,
        )
        raise err


def delete_object(object_type: ObjectType, id_: str) -> None:
    """
    Delete an object by ID.

    Args:
        object_type: The object type.
        id_: The HubSpot ID.

    Returns:
        None
    """

    if isinstance(id_, int):
        id_ = str(id_)

    if not isinstance(id_, str) or not id_.isdigit():
        raise InvalidRequestError(f"Invalid object ID: {id_!r}")

    try:
        api = get_api_interface_by_object_name(_client, object_type)
        logger.debug(f"Deleting {object_type.value.capitalize()} object by id={id_!r}")
        api.basic_api.archive(contact_id=id_)
        logger.info(f"Deleted {object_type.value.capitalize()} object: id={id_!r}")
    except ApiException as exc:
        err = map_hubspot_exception(exc)

        if isinstance(err, ObjectNotFoundError):
            logger.warning(
                f"{object_type.value.capitalize()} "
                f"object not found during delete: id={id_}"
            )
            return None

        logger.error(
            f"Failed to delete {object_type.value.capitalize()} with id={id_}: {err}",
            exc_info=True,
        )
        raise err


def create_object(
    object_type: ObjectType,
    properties: dict[str, Any],
    associations: dict[str, str] | None,
) -> dict:
    """
    Create a new HubSpot object.

    Args:
        object_type: The type of object to create.
        properties: Field values for the new object.
        associations: Associations for the new object.

    Returns:
        The created object.
    """

    try:
        api = get_api_interface_by_object_name(_client, object_type)
        logger.debug(
            f"Creating {object_type.value.capitalize()} "
            f"object with properties={properties!r}"
        )
        obj = api.basic_api.create(
            SimplePublicObjectInputForCreate(
                associations=associations, properties=properties
            )
        )
        logger.info(
            f"Created new {object_type.value.capitalize()} "
            f"object with properties={properties!r}"
        )
        return obj
    except ApiException as exc:
        err = map_hubspot_exception(exc)

        logger.error(
            f"Failed to create {object_type.value.capitalize()} object: {err}",
            exc_info=True,
        )
        raise err


def get_all_properties(object_type: ObjectType):
    return get_client().crm.properties.core_api.get_all(object_type.value.lower())
