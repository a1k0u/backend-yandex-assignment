import connection
from responses import _validation_fail, _send_result_process, _item_not_found
import db_requests as req
from models import create_product, Type


@connection.connect_to_db
def import_goods_to_db(conn, items):
    for item in items.get("items", []):
        product = create_product(item, items["updateDate"])
        result = req.check_item_in_db(conn, product)

        temporary = product.uuid
        product.uuid = product.parent_id
        if product.uuid is not None:
            element = req.check_item_in_db(conn, product)
            if not element or element[0][1] == Type.OFFER.name:
                return _validation_fail()
        product.uuid = temporary

        if not result:
            req.insert_item_into_db(conn, product)
        else:
            group_status = result[0][1]
            if group_status != product.group:
                return _validation_fail()
            req.update_item_in_db(conn, product)
    return _send_result_process()


@connection.connect_to_db
def delete_goods_from_db(conn, node_id):
    element = req.take_element_by_uuid(conn, node_id)
    if not element:
        return _item_not_found()

    uuids_to_check = set()
    uuids_to_delete = {node_id}

    element_status, element_uuid = element[0][2], element[0][0]
    if element_status == Type.CATEGORY.name:
        uuids_to_check.add(element_uuid)

    while uuids_to_check:
        items = req.find_by_parent_id(conn, uuids_to_check.pop())
        for uuid, group in items:
            uuids_to_delete.add(uuid)
            if group == Type.CATEGORY.name:
                uuids_to_check.add(uuid)

    for uuid in uuids_to_delete:
        req.delete_item_from_db(conn, uuid)
    return _send_result_process()
