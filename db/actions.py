"""
All actions with a database for routes in main.py.
"""

from typing import Tuple
import datetime
import sys
import os

from objects.variables import (
    create_product_from_dict,
    Type,
    Product,
    create_str_from_time,
    create_time_from_str,
)
from db.connection import connect_to_db
from utils.validator import validate_uuid, validate_import, validate_time
from utils.logger import log_db, log_validator, log_route
import objects.responses as response
import db.requests as request


def __create_response_unit(element: Product) -> dict:
    """
    Creates element (dict) for future
    response which will convert into a json.
    """

    return dict(
        id=element.id,
        name=element.name,
        type=element.type,
        parentId=element.parent_id,
        date=create_str_from_time(element.date),
        price=element.price,
        children=None,
    )


def __update_elements_date(conn, elements: set, date: datetime) -> None:
    """
    Update date of categories which elements
    were inserted/updated in import.
    """

    checked = {None}
    while elements:
        element = elements.pop()
        if element not in checked:

            request.update_element_time_by_id(conn, element, date)
            log_db.debug(f"Time of {element} was updated.")
            element_value = request.get_element_by_id(conn, element)

            if element_value and element_value.parent_id not in checked:
                elements.add(element_value.parent_id)

        checked.add(element)


@connect_to_db
def import_goods_to_db(conn, items) -> Tuple[dict, int]:
    """
    Imports categories and offers.

    If import data is invalid, two elements
    with equal uuid in one request or element type
    was changed, response will with status code 400.

    If element was in a database, it will just update their data.
    In an opposite situation it will insert in DB.
    """

    if not validate_import(items):
        return response.validation_fail_response()

    elements_to_update_time = {None}
    for item in items.get("items", []):

        product: Product = create_product_from_dict(item, items["updateDate"])
        result = request.get_element_by_id(conn, product.id)
        elements_to_update_time.add(product.parent_id)

        if product.parent_id is not None:
            parent_element = request.get_element_by_id(conn, product.parent_id)
            if not parent_element or parent_element.type == Type.OFFER.value:
                log_db.warning(
                    f"No parent element in DB or parent of {product.id} is an offer."
                )
                return response.validation_fail_response()

        if not result:
            request.insert_element(conn, product)
            log_db.debug(f"{product.id=} was inserted in database.")
            continue

        if result.type != product.type:
            log_db.warning(
                f"Tries to change element type from "
                f"{product.type} to {result.type}, {product.id=}"
            )
            return response.validation_fail_response()

        request.update_element_by_id(conn, product)
        log_db.debug(f"{product.id=} was updated in a database.")

    date = create_time_from_str(items["updateDate"])
    __update_elements_date(conn, elements_to_update_time, date)
    log_db.debug("All related items have updated their date.")

    return response.success_response()


def __delete_related_goods(conn, node_id: str) -> None:
    """
    Deletes from a database.

    Deletes categories and elements (offers, subcategories)
    which are connecting with it by parend_id.
    Deletes offer.

    :param node_id: current element to delete.
    """

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
def delete_goods_from_db(conn, node_id: str) -> Tuple[dict, int]:
    """
    Delete element in a database by node_id.

    If id is a category, elements which are connected
    with this node_id will be deleted too.

    :returns results of deleting (dict and a status code).
    """

    if not validate_uuid(node_id):
        log_validator.warning(f"Invalid uuid={node_id} in delete.")
        return response.validation_fail_response()

    element = request.get_element_by_id(conn, node_id)
    if not element:
        log_db.warning(f"Delete. Element doesn't exist, {node_id=}.")
        return response.element_not_found_response()

    __delete_related_goods(conn, node_id)
    log_db.debug(f"All related with {node_id=} were deleted.")

    return response.success_response()


def __export_related_goods(
    conn, node_id: str, summa: int, counter: int
) -> Tuple[dict, int, int]:
    """
    Recursive chain which gets all offers and
    subcategories of node_id if it is a category,
    and price of category is an average sum of all offers.
    In other words, average of all leafs in a tree.

    If node_id is an offer, function will return dict
    with all information about this element.

    :param node_id: the element which is researching now.
    :param summa: summa of all prices of offers in a tree.
    :param counter: elements (leafs) in a tree.
    :return: dict with information about current root,
            summa of prices of leafs and counting of leafs.
    """

    element = request.get_element_by_id(conn, node_id)
    unit = __create_response_unit(element)
    log_db.debug(f"Unit of response for {node_id=} was created.")

    if unit["type"] == Type.CATEGORY.value:
        children = request.get_elements_by_parent_id(conn, unit["id"])
        log_db.debug(f"Got children of category {unit['id']=}.")
        unit["children"] = [] if children else None

        for child in children:
            unit_child, __summa, __counter = __export_related_goods(
                conn, child.id, 0, 0
            )
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
def export_goods_from_db(conn, node_id: str) -> Tuple[dict, int]:
    """
    Exports offer by id or category with subcategories
    and children-offers.

    Price of category is an average sum of all offers on a category.
    :return dict with items and status code.
    """

    if not validate_uuid(node_id):
        log_validator.warning(f"Invalid in export goods, uuid={node_id}.")
        return response.validation_fail_response()

    element = request.get_element_by_id(conn, node_id)
    if not element:
        log_db.warning(f"Export goods. Element doesn't exist, {node_id=}.")
        return response.element_not_found_response()

    result, *extra = __export_related_goods(conn, node_id, 0, 0)
    log_route.debug("Export goods was successful.")

    return result, 200


@connect_to_db
def export_sales_from_db(conn, date: str) -> Tuple[dict, int]:
    """
    Exports all offers which was updated
    for 24 hours from date.

    :return dict with offers and status code.
    """

    if not validate_time(date):
        log_validator.warning(f"Time in export sales wasn't validated, {date=}")
        return response.validation_fail_response()

    date = create_time_from_str(date)
    _response = {"items": []}

    date_start = date - datetime.timedelta(hours=24)
    elements = request.get_offers_by_time_period(conn, date_start, date)

    log_db.debug("Got all items which was update for 24 hours.")

    for element in elements:
        unit = __create_response_unit(element)
        unit.pop("children")
        _response["items"].append(unit)

    log_route.debug("Export sales was successful.")

    return _response, 200
