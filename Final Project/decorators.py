from functools import wraps
from flask import request


def validate_form(fields):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if request.method == "POST":
                for field in fields:
                    if not request.form.get(field):
                        return f"Missing field: {field}"
            return func(*args, **kwargs)
        return wrapper
    return decorator