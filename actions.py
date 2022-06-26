import connection
import db_requests as req
from models import create_product, Type


@connection.connect_to_db
def import_goods_to_db(conn, items) -> int:
    for item in items.get("items", []):
        product = create_product(item, items["updateDate"])
        result = req.check_item_in_db(conn, product)

        temporary = product.uuid
        product.uuid = product.parent_id
        if product.uuid is not None and not check_item_in_db(cursor, product):
            return 400
        product.uuid = temporary

        if not result:
            insert_item_into_db(conn, product)
        else:
            group_status = result[0][1]
            if group_status != product.group:
                return 400
            update_item_in_db(conn, product)
    return 200


@connection.connect_to_db
def delete_goods_from_db(node_id):
    uuids_to_check = {node_id}
    uuids_to_delete = {node_id}

    while uuids_to_check:
        items = db_request(find_by_parent_id, uuids_to_check.pop())
        for uuid, group in items:
            uuids_to_delete.add(uuid)
            if group == "CATEGORY":
                uuids_to_check.add(uuid)

    code = 200

    connection = create_connection()
    if connection is None:
        return 500
    cursor = connection.cursor()

    for uuid in uuids_to_delete:
        delete_item_from_db(cursor, uuid)

    connection.commit()
    cursor.close()
    return code
