from utils.validator import validate_import
from db.database import import_goods_to_db

from flask import Flask, jsonify, request
from json import loads

app = Flask(__name__)


@app.route("/imports", methods=["POST"])
def import_goods():
    data = loads(request.data.decode())
    if not validate_import(data):
        return jsonify(dict(code=400, message="Validation Failed")), 400
    return jsonify(dict(code=import_goods_to_db(data)))


@app.errorhandler(404)
def error_page(error):
    return jsonify(dict(code=404, message="Error"))


if __name__ == "__main__":
    app.run(debug=True)
