from typing import Tuple

from flask import jsonify, Response


def validation_fail() -> Tuple[Response, int]:
    return jsonify(dict(code=400, message="Validation Failed")), 400


def item_not_found() -> Tuple[Response, int]:
    return jsonify(dict(code=404, message="Item not found")), 404


def page_not_found() -> Tuple[Response, int]:
    return jsonify(dict(code=404, message="Page not found")), 404


def send_success() -> Tuple[Response, int]:
    return jsonify(dict(code=200)), 200
