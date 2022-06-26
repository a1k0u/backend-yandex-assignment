from typing import Tuple

from validator import validate_import, validate_uuid
from models import create_product
from db.database import import_goods_to_db, delete_goods_from_db
from requests import db_request, check_item

import flask
from flask import Flask, jsonify, request, Response
from json import loads

app = Flask(__name__)


def _validation_fail() -> Tuple[Response, int]:
    return jsonify(dict(code=400, message="Validation Failed")), 400


def _item_not_found() -> Tuple[Response, int]:
    return jsonify(dict(code=404, message="Item not found")), 404


def _page_not_found() -> Tuple[Response, int]:
    return jsonify(dict(code=404, message="Page not found")), 404


def _success_process() -> Tuple[Response, int]:
    return jsonify(dict(code=200)), 200


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

    import_goods_to_db(data)

    return _success_process()


@app.route("/delete/<node_id>", methods=["DELETE"])
def delete_goods(node_id):
    if not validate_uuid(node_id):
        return _validation_fail()

    product = create_product({"id": node_id}, "")

    result = db_request(check_item, product)

    if not result:
        return _item_not_found()

    delete_goods_from_db(node_id)

    return _success_process()


@app.route("/nodes/<node_id>", methods=["GET"])
def import_node(node_id):
    if not validate_uuid(node_id):
        return _validation_fail()

    product = create_product({"id": node_id}, "")
    result = db_request(check_item, product)

    if not result:
        return _item_not_found()

    return 500


@app.errorhandler(404)
def error_page(error):
    return _page_not_found()


if __name__ == "__main__":
    app.run(debug=True)
