from flask import jsonify, Response

from typing import Tuple


def _validation_fail() -> Tuple[Response, int]:
    return jsonify(dict(code=400, message="Validation Failed")), 400


def _item_not_found() -> Tuple[Response, int]:
    return jsonify(dict(code=404, message="Item not found")), 404


def _page_not_found() -> Tuple[Response, int]:
    return jsonify(dict(code=404, message="Page not found")), 404


def _send_result_process(code=200) -> Tuple[Response, int]:
    return jsonify(dict(code=code)), 200
