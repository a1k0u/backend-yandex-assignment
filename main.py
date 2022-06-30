"""
check ./doc/openapi.yaml

/imports            - POST
/delete/<node_id>   - DELETE
/nodes/<node_id>    - GET
"""

import json

from flask import Flask, request, jsonify
import flask.wrappers

from db.actions import import_goods_to_db, delete_goods_from_db, export_goods_from_db, export_sales_from_db
from db.connection import serialize_data
from utils.validator import validate_import, validate_uuid, validate_time
from utils.logger import log_route
import objects.responses as response


app = Flask(__name__)


def _get_data(req):
    try:
        return json.loads(req.data.decode())
    except json.decoder.JSONDecodeError:
        log_route.warning("Got error while unpacking data.")
    return {}


@app.route("/imports", methods=["POST"])
def import_goods():
    data = _get_data(request)
    _response, _code = import_goods_to_db(data)
    return _response, _code


@app.route("/delete/<node_id>", methods=["DELETE"])
def delete_goods(node_id):
    _response, _code = delete_goods_from_db(node_id)
    return _response, _code


@app.route("/nodes/<node_id>", methods=["GET"])
def export_goods(node_id):
    _response, _code = export_goods_from_db(node_id)
    return _response, _code


@app.route("/sales", methods=["GET"])
def export_sales():
    date = request.args.get("date", "")
    _response, _code = export_sales_from_db(date)
    return _response, _code


@app.errorhandler(404)
def error_page(error):
    log_route.debug(f"Page not found. {error=}")
    return serialize_data(response.page_not_found_response())


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
