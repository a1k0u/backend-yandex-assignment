"""
The main center of validating data.
Check ../doc/openapi.yaml.
"""

from datetime import datetime
from typing import Any
from uuid import UUID

from utils.logger import log_validator
from objects.variables import Type, create_time_from_str


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
        create_time_from_str(time)
    except ValueError:
        return False
    return True


def validate_price(num: Any) -> int:
    """
    Validates price. Price has to be integer.
    If price is str, None or etc. will return -1.
    """

    try:
        return int(num)
    except (ValueError, TypeError):
        return -1


def validate_item(item: dict) -> bool:
    """
    Validates by name, type and price specific.
    """

    if item.get("name") is None:
        log_validator.warning(f"The Name field is empty, {item.get('id')=}.")
        return False

    if item.get("type") is None:
        log_validator.warning(f"The Type field is empty, {item.get('id')=}.")
        return False

    if item.get("type") not in [el.value for el in Type]:
        log_validator.warning(
            f"This type isn't exist `{item.get('type')=}`, {item.get('id')=}"
        )
        return False

    if item.get("type") == Type.OFFER.value and validate_price(item.get("price")) < 0:
        log_validator.warning(
            f"Offer has negative price, null or incorrect format, {item.get('id')=}"
        )
        return False

    if item.get("type") == Type.CATEGORY.value and item.get("price") is not None:
        log_validator.warning(
            f"The category is not zero, it has a price, {item.get('id')=}."
        )
        return False

    return True


def validate_import(data: dict) -> bool:
    """
    Validates import data (time, items).
    """

    time = data.get("updateDate", "")
    if not validate_time(time):
        log_validator.warning(f"Incorrect time, got: {time}.")
        return False

    uuids = {None}
    for item in data.get("items", []):

        item_id = item.get("id", None)
        if item_id in uuids or not validate_uuid(item_id):
            log_validator.warning(
                f"Got two equal uuids in one request or uuid is invalid, {item_id=}."
            )
            return False
        uuids.add(item_id)

        if not validate_item(item):
            log_validator.warning(f"Data validation was unsuccessful, {item_id=}")
            return False

        log_validator.debug(f"Item={item_id} validation was successful.")

    log_validator.debug(f"Data validation was successful, {time=}")
    return True


if __name__ == "__main__":
    print(validate_uuid("3fa85f64-5717-4562-b3fc-2c963f66a444"))
