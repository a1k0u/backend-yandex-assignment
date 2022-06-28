"""
Exceptions for REST API application.
"""


class DatabaseError(Exception):
    def __init__(self, error):
        self.error = error
