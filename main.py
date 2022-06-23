from utils.validator import validate_import
from utils.models import create_product, Product
from db.database import import_goods_to_db
from db.requests import db_request, check_item


from flask import Flask, jsonify, request
from json import loads

app = Flask(__name__)


@app.route("/imports", methods=["POST"])
def import_goods():
    data = loads(request.data.decode())
    if not validate_import(data):
        return jsonify(dict(code=400, message="Validation Failed")), 400
    code = import_goods_to_db(data)
    return jsonify(dict(code=code)), code


@app.route("/delete/<node_id>", methods=["DELETE"])
def delete_goods(node_id):
    if not validate_import(node_id):
        return jsonify(dict(code=400, message="Validation Failed")), 400
    product = create_product({"id": node_id}, "")
    result = db_request(check_item, product)
    if not result:
        return jsonify(dict(code=404, message="Item not found")), 404


@app.errorhandler(404)
def error_page(error):
    return jsonify(dict(code=404, message="Error"))


if __name__ == "__main__":
    app.run(debug=True)
