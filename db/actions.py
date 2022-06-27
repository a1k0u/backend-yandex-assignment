import sys
import os

from typing import List

from objects.responses import validation_fail, send_success, item_not_found
from objects.variables import create_product, Type
from db.connection import connect_to_db
from utils.logger import log_db
import db.requests as req


def __process_node_id(conn, node_id, to_check: set):
    element = req.take_element_by_uuid(conn, node_id)
    if not element:
        return item_not_found()

    element_status, element_uuid = element[0][2], element[0][0]
    if element_status == Type.CATEGORY.name:
        to_check.add(element_uuid)

    return None


@connect_to_db
def import_goods_to_db(conn, items):
    for item in items.get("items", []):
        product = create_product(item, items["updateDate"])
        result = req.check_item_in_db(conn, product)

        temporary = product.uuid
        product.uuid = product.parent_id
        if product.uuid is not None:
            element = req.check_item_in_db(conn, product)
            if not element or element[0][1] == Type.OFFER.name:
                log_db.warning("No parent element or uuid parent is a offer.")
                return validation_fail()
        product.uuid = temporary

        if not result:
            req.insert_item_into_db(conn, product)
        else:
            group_status = result[0][1]
            if group_status != product.group:
                log_db.warning("Invalid data: tries to change element type.")
                return validation_fail()
            req.update_item_in_db(conn, product)
    return send_success()


@connect_to_db
def delete_goods_from_db(conn, node_id):
    uuids_to_check, uuids_to_delete = set(), {node_id}

    answer = __process_node_id(conn, node_id, uuids_to_check)
    if answer is not None:
        return answer

    while uuids_to_check:
        items = req.find_by_parent_id(conn, uuids_to_check.pop())
        for uuid, group in items:
            uuids_to_delete.add(uuid)
            if group == Type.CATEGORY.name:
                uuids_to_check.add(uuid)

    for uuid in uuids_to_delete:
        req.delete_item_from_db(conn, uuid)
    return send_success()


def __create_response_unit(element) -> dict:
    _id, _name, _type, _parent_id, _price, _time = element[0]
    return dict(
        id=_id,
        name=_name,
        type=_type,
        parentId=_parent_id,
        date=_time,
        price=_price,
        children=None,
    )


@connect_to_db
def export_nodes_from_db(conn, node_id):
    element = req.take_element_by_uuid(conn, node_id)
    if not element:
        return item_not_found()

    unit = __create_response_unit(element)
    if unit["type"] == Type.CATEGORY.name:
        children = req.find_by_parent_id(conn, unit["id"])
        unit["children"] = [] if children else None

        for child in children:
            unit["children"].append(export_nodes_from_db(child[0])[0])
            unit["price"] = unit["children"][-1]["price"] + (
                0 if unit.get("price") is None else unit["price"]
            )

        unit["price"] = None if not children else (unit["price"] // len(children))
    return unit, 200
