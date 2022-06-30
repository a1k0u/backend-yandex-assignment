import datetime
from typing import List
import sys
import os

from objects.variables import create_product_from_dict, Type, Product, create_str_from_time, create_time_from_str
from db.connection import connect_to_db
from utils.validator import validate_uuid, validate_import, validate_time
from utils.logger import log_db
import objects.responses as response
import db.requests as request


def __create_response_unit(element: Product) -> dict:
    return dict(
        id=element.id,
        name=element.name,
        type=element.type,
        parentId=element.parent_id,
        date=create_str_from_time(element.date),
        price=element.price,
        children=None,
    )


def __update_elements_date(conn, elements: set, date) -> None:
    checked = {None}
    while elements:
        element = elements.pop()
        if element not in checked:

            request.update_element_time_by_id(conn, element, date)
            log_db.debug(f"the time of {element} was updated.")
            element_value = request.get_element_by_id(conn, element)

            if element_value and element_value.parent_id not in checked:
                elements.add(element_value.parent_id)

        checked.add(element)


@connect_to_db
def import_goods_to_db(conn, items):
    if not validate_import(items):
        return response.validation_fail_response()

    elements_to_update_time = set()
    for item in items.get("items", []):

        product: Product = create_product_from_dict(item, items["updateDate"])
        result = request.get_element_by_id(conn, product.id)
        elements_to_update_time.add(product.parent_id)

        if product.parent_id is not None:
            parent_element = request.get_element_by_id(conn, product.parent_id)
            if not parent_element or parent_element.type == Type.OFFER.value:
                log_db.warning(
                    f"No parent element in DB or parent of {product.id} is a offer."
                )
                return response.validation_fail_response()

        if not result:
            request.insert_element(conn, product)
            log_db.debug(f"{product.id=} was inserted in database.")
            continue

        if result.type != product.type:
            log_db.warning(
                f"Tries to change element type from {product.type} to {result.type}, {product.id=}"
            )
            return response.validation_fail_response()

        request.update_element_by_id(conn, product)
        log_db.debug(f"{product.id=} was updated in database.")

    __update_elements_date(conn, elements_to_update_time, items["updateDate"])
    log_db.debug("All related items have updated their date.")

    return response.success_response()


def __delete_related_goods(conn, node_id):
    element = request.get_element_by_id(conn, node_id)

    children = (
        request.get_elements_by_parent_id(conn, node_id)
        if element.type == Type.CATEGORY.value
        else []
    )

    for child in children:
        __delete_related_goods(conn, child.id)

    request.delete_element_by_id(conn, node_id)
    log_db.debug(f"{node_id=} was deleted.")


@connect_to_db
def delete_goods_from_db(conn, node_id):
    if not validate_uuid(node_id):
        log_route.warning(f"Invalid uuid={node_id}.")
        return response.validation_fail_response()

    element = request.get_element_by_id(conn, node_id)
    if not element:
        log_db.warning(f"Element doesn't exist, {node_id=}.")
        return response.element_not_found_response()

    __delete_related_goods(conn, node_id)
    log_db.debug(f"All related with {node_id=} were deleted.")

    return response.success_response()


def __export_related_goods(conn, node_id, summa, counter):
    element = request.get_element_by_id(conn, node_id)
    unit = __create_response_unit(element)
    log_db.debug(f"Unit of response for {node_id=} was created.")

    if unit["type"] == Type.CATEGORY.value:
        children = request.get_elements_by_parent_id(conn, unit["id"])
        unit["children"] = [] if children else None

        for child in children:
            unit_child, __summa, __counter = __export_related_goods(conn, child.id, 0, 0)
            unit["children"].append(unit_child)

            last_added_child = unit["children"][-1]

            if last_added_child["type"] == Type.OFFER.value:
                summa += last_added_child["price"]
                counter += 1

            if last_added_child["type"] == Type.CATEGORY.value:
                summa += __summa
                counter += __counter

        unit["price"] = None if not children else (summa // counter)

    return unit, summa, counter


@connect_to_db
def export_goods_from_db(conn, node_id):
    if not validate_uuid(node_id):
        log_route.warning(f"Invalid uuid={node_id}.")
        return response.validation_fail_response()

    element = request.get_element_by_id(conn, node_id)
    if not element:
        log_db.warning(f"Element doesn't exist, {node_id=}.")
        return response.element_not_found_response()

    result, *extra = __export_related_goods(conn, node_id, 0, 0)
    log_db.debug("Export was successful.")

    return result, 200


@connect_to_db
def export_sales_from_db(conn, date: str):
    if not validate_time(date):
        return response.validation_fail_response()

    date = create_time_from_str(date)
    _response = {"items": []}
    elements = request.get_offers_by_time(conn, date)

    for element in elements:
        unit = __create_response_unit(element)
        unit.pop("children")
        _response["items"].append(unit)

    return _response, 200
