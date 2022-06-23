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


def validate_item(item) -> bool:
    if item["name"] is None:
        return False

    if item["type"] == "OFFER" and (item.get("price") is None or item["price"] < 0):
        return False

    if item["type"] == "CATEGORY" and item["price"] is not None:
        return False

    return True


def validate_import(data) -> bool:
    if not validate_time(data.get("updateDate", "")):
        return False

    uuids = {None}

    for item in data.get("items", []):
        if item.get("id", None) in uuids or not validate_uuid(item.get("id", None)):
            return False
        uuids.add(item["id"])

        if not validate_item(item):
            return False
    return True
