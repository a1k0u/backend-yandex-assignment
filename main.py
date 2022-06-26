"""
check ./doc/openapi.yaml

/imports            - POST
/delete/<node_id>   - DELETE
/nodes/<node_id>    - GET
"""

import json

from flask import Flask, request

from db.actions import import_goods_to_db, delete_goods_from_db
from utils.validator import validate_import, validate_uuid
from objects.responses import _validation_fail, _page_not_found
from utils.log import log_route

app = Flask(__name__)


def _get_data(req):
    try:
        return json.loads(req.data.decode())
    except json.decoder.JSONDecodeError:
        log_route.warning("Error. While unpacking data.")
        return {}


@app.route("/imports", methods=["POST"])
def import_goods():
    """Gets data(offers, categories), validates and puts into database."""
    data = _get_data(request)

    if not validate_import(data):
        log_route.warning("Validation failed.")
        return _validation_fail()

    return import_goods_to_db(data)


@app.route("/delete/<node_id>", methods=["DELETE"])
def delete_goods(node_id):
    """Delete offers or category with subcategories and children offers."""
    if not validate_uuid(node_id):
        log_route.warning("Invalid uuid.")
        return _validation_fail()

    return delete_goods_from_db(node_id)


# @app.route("/nodes/<node_id>", methods=["GET"])
# def import_node(node_id):
#     if not validate_uuid(node_id):
#         return _validation_fail()
#
#     product = create_product({"id": node_id}, "")
#     result = db_request(check_item_in_db, product)
#
#     if not result:
#         return _item_not_found()
#
#     return 500


@app.errorhandler(404)
def error_page(error):
    """If URL doesn't exit, user will get error-json."""
    log_route.debug(f"Page not found; {error=}")
    return _page_not_found()


if __name__ == "__main__":
    app.run(debug=True)
