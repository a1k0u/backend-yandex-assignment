import connection
from requests import db_request, insert_item, delete_item, update_item, find_by_parent_id,check_item, create_connection
from models import create_product


@connection.connect
def import_goods_to_db(connection, items) -> int:
    code = 200
    cursor = connection.cursor()

    for item in items["items"]:
        product = create_product(item, items["updateDate"])
        result = check_item(cursor, product)

        parent = product.uuid
        product.uuid = product.parent_id
        if product.uuid is not None and not check_item(cursor, product):
            code = 400
            break
        product.uuid = parent

        if not result:
            insert_item(cursor, product)
        else:
            status = result[0][1]
            if status != product.group:
                code = 400
                break

            update_item(cursor, product)
    else:
        connection.commit()

    cursor.close()
    return code


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
        delete_item(cursor, uuid)

    connection.commit()
    cursor.close()
    return code
