from typing import Tuple

from validator import validate_import, validate_uuid
from models import create_product
from actions import import_goods_to_db, delete_goods_from_db
import db_requests as req
from responses import _validation_fail

import flask
from flask import Flask, jsonify, request, Response
from json import loads


app = Flask(__name__)


def _get_data(req):
    try:
        return loads(req.data.decode())
    except ...:
        return {}


@app.route("/imports", methods=["POST"])
def import_goods():
    data = _get_data(request)

    if not validate_import(data):
        return _validation_fail()

    return import_goods_to_db(data)


@app.route("/delete/<node_id>", methods=["DELETE"])
def delete_goods(node_id):
    if not validate_uuid(node_id):
        return _validation_fail()

    return delete_goods_from_db(node_id)


@app.route("/nodes/<node_id>", methods=["GET"])
def import_node(node_id):
    if not validate_uuid(node_id):
        return _validation_fail()

    product = create_product({"id": node_id}, "")
    result = db_request(check_item_in_db, product)

    if not result:
        return _item_not_found()

    return 500


@app.errorhandler(404)
def error_page(error):
    return _page_not_found()


if __name__ == "__main__":
    app.run(debug=True)
