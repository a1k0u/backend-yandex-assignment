"""
The main center of validating data.
Check ../doc/openapi.yaml.
"""

from datetime import datetime
from uuid import UUID

from utils.logger import log_validator
from objects.variables import Type


def validate_uuid(uuid: str) -> bool:
    """
    Validates uuid (element's id) by uuid module.
    """

    try:
        UUID(uuid)
    except ValueError:
        return False
    return True


def validate_time(time: str) -> bool:
    """
    Validates time in ISO 8601 format.
    """

    try:
        datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        return False
    return True


def validate_price(num) -> int:
    """
    Validates price. Price has to be integer.
    If price is str, None or etc. will return -1.
    """

    try:
        return int(num)
    except (ValueError, TypeError):
        return -1

# TODO: logger
def validate_item(item) -> bool:
    """Validates by name, type and price specific."""

    if item.get("name") is None:
        log_validator.debug(f"Name field is empty, {item.get('id')=}.")
        return False

    if item.get("type") is None:
        log_validator.debug("Type field is empty.")
        return False

    if item.get("type") not in (Type.OFFER.name, Type.CATEGORY.name):
        log_validator.debug("Type isn't in the list.")
        return False

    if item.get("type") == Type.OFFER.name and validate_price(item.get("price")) < 0:
        log_validator.debug("Offer has negative price or null.")
        return False

    if item.get("type") == Type.CATEGORY.name and item.get("price") is not None:
        log_validator.debug("Category doesn't null, have price.")
        return False

    return True


def validate_import(data: dict) -> bool:
    """Validates import data."""
    time = data.get("updateDate", "")
    if not validate_time(time):
        log_validator.debug(f"Incorrect time, got: {time}")
        return False

    uuids = {None}
    for item in data.get("items", []):
        item_id = item.get("id", None)
        if item_id in uuids or not validate_uuid(item_id):
            log_validator.debug("Got two or equal uuids in one request.")
            return False
        uuids.add(item["id"])

        if not validate_item(item):
            return False
    return True


if __name__ == "__main__":
    print(validate_uuid("3fa85f64-5717-4562-b3fc-2c963f66a444"))
