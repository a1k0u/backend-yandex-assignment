import sys
import os

from typing import List

from objects.responses import validation_fail, success_request, element_not_found
from objects.variables import create_product_from_dict, Type, Product
from db.connection import connect_to_db
from utils.logger import log_db
import db.requests as req


def create_response_unit(element: Product) -> dict:
    return dict(
        id=element.id,
        name=element.name,
        type=element.type,
        parentId=element.parent_id,
        date=element.date,
        price=element.price,
        children=None,
    )


@connect_to_db
def import_goods_to_db(conn, items):
    elements_to_update_time = set()
    for item in items.get("items", []):
        product = create_product_from_dict(item, items["updateDate"])
        result = req.get_element_by_id(conn, product.id)
        elements_to_update_time.add(product.parent_id)

        temporary = product.id
        product.id = product.parent_id
        if product.id is not None:
            element = req.get_element_by_id(conn, product.id)
            if not element or element.type == Type.OFFER.name:
                log_db.warning("No parent element or uuid parent is a offer.")
                return validation_fail()
        product.id = temporary

        if not result:
            req.insert_element(conn, product)
        else:
            if result.type != product.type:
                log_db.warning("Invalid data: tries to change element type.")
                return validation_fail()
            req.update_element_by_id(conn, product)

    checked = {None}
    while elements_to_update_time:
        element = elements_to_update_time.pop()
        if element not in checked:
            req.update_element_time_by_id(conn, element, items["updateDate"])
            element_value = req.get_element_by_id(conn, element)
            if element_value and element_value.parent_id not in checked:
                elements_to_update_time.add(element_value.parent_id)
        checked.add(element)

    return success_request()


@connect_to_db
def delete_goods_from_db(conn, node_id):
    element = req.get_element_by_id(conn, node_id)
    if not element:
        return element_not_found()

    children = (
        req.get_elements_by_parent_id(conn, element.id)
        if element.type == Type.CATEGORY.name
        else []
    )
    for child in children:
        delete_goods_from_db(child.id)

    req.delete_element_by_id(conn, node_id)
    return success_request()


@connect_to_db
def export_nodes_from_db(conn, node_id):
    element = req.get_element_by_id(conn, node_id)
    if not element:
        return *element_not_found(), 0, 0

    unit = create_response_unit(element)
    summa, counter = 0, 0
    if unit["type"] == Type.CATEGORY.name:
        children = req.get_elements_by_parent_id(conn, unit["id"])
        unit["children"] = [] if children else None

        for child in children:
            unit_child, code, _summa, _counter = export_nodes_from_db(child.id)
            unit["children"].append(unit_child)

            previous_child = unit["children"][-1]
            if previous_child["type"] == Type.OFFER.name:
                counter += 1
                summa += previous_child["price"]
            if previous_child["type"] == Type.CATEGORY.name:
                summa += _summa
                counter += _counter

        unit["price"] = None if not children else (summa // counter)
    return unit, 200, summa, counter
