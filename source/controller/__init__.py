from functools import wraps

from flask import request, jsonify
from flask_sqlalchemy import BaseQuery
from pydantic import BaseModel, ValidationError
from error import error_type
import Messages

# item pagination
def paginate(query: BaseQuery, page: int = 1, rows_per_page: int = 1):

    pagination = query.paginate(page=page, per_page=rows_per_page, error_out=False)

    data = pagination.items

    output = {
        "pagination": {
            "pages_count": pagination.pages,
            "itens_count": pagination.total,
            "itens_per_page": rows_per_page,
            "prev": pagination.prev_num,
            "next": pagination.next_num,
            "current": pagination.page,
        },
        "itens": [],
        "error": False,
    }

    return data, output


def field_validator(validator: BaseModel):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            data = request.get_data()

            try:
                validator.parse_raw(data)
            except ValidationError as e:
                for error in e.errors():
                    msg = error_type.get(error["type"])
                    ctx = error.get("ctx")

                    if msg:
                        if ctx:
                            msg = msg.format(**ctx)
                        error["msg"] = msg

                validation_errors = {"body_params": e.errors()}

                return (
                    jsonify(
                        {
                            "validation_error": validation_errors,
                            "status_code": 400,
                        }
                    ),
                    400,
                )

            return f(*args, **kwargs)

        return wrapped

    return wrapper
