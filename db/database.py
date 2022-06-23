from db.requests import db_request, insert_item, update_item, check_item, create_connection
from utils.models import Product, create_product
from utils.exceptions import DBError


def import_goods_to_db(items) -> int:
    code = 200

    connection = create_connection()
    if connection is None:
        return 500
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


def delete_goods():
    ...
