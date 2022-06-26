from models import Type

from datetime import datetime
from uuid import UUID


def validate_uuid(uuid: str) -> bool:
    try:
        version = UUID(uuid).version
    except ValueError:
        return False
    return True


def validate_time(time: str) -> bool:
    try:
        datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        return False
    return True


def validate_price(num) -> float:
    try:
        return float(num)
    except ValueError:
        return -1


def validate_item(item) -> bool:
    if item.get("name") is None:
        return False

    if item.get("type") is None:
        return False

    if item.get("type") not in (Type.OFFER, Type.CATEGORY):
        return False

    if item.get("type") == Type.OFFER and validate_price(item.get("price")) < 0:
        return False

    if item.get("type") == Type.CATEGORY and item.get("price") is not None:
        return False

    return True


def validate_import(data: dict) -> bool:
    if not validate_time(data.get("updateDate", "")):
        return False

    uuids = {None}
    for item in data.get("items", []):
        item_id = item.get("id", None)
        if item_id in uuids or not validate_uuid(item_id):
            return False
        uuids.add(item["id"])

        if not validate_item(item):
            return False
    return True
