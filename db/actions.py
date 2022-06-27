import sys
import os

from typing import List

from objects.responses import validation_fail, send_success, item_not_found
from objects.variables import create_product, Type
from db.connection import connect_to_db
from utils.logger import log_db
import db.requests as req


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
    element = req.take_element_by_uuid(conn, node_id)
    if not element:
        return item_not_found()

    children = (
        req.find_by_parent_id(conn, element[0][0])
        if element[0][2] == Type.CATEGORY.name
        else []
    )
    for child in children:
        delete_goods_from_db(child[0])

    req.delete_item_from_db(conn, node_id)
    return send_success()


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
