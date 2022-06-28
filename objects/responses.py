"""
Contains various answers for routes.
Returns a status code and  a dictionary with a code, message.
"""

from typing import Tuple


def validation_fail() -> Tuple[dict, int]:
    return dict(code=400, message="Validation Failed"), 400


def element_not_found() -> Tuple[dict, int]:
    return dict(code=404, message="Item not found"), 404


def page_not_found() -> Tuple[dict, int]:
    return dict(code=404, message="Page not found"), 404


def success_request() -> Tuple[dict, int]:
    return dict(code=200, message="OK"), 200


def custom_request(code: int = 200, message: str = "OK") -> Tuple[dict, int]:
    return dict(code=code, message=message), code
