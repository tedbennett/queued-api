import uuid

from error import ApiError
from utils import (
    _extract_path_param,
    _extract_body,
    _get_table,
    _get_user,
    _success_response,
    _process_api_error,
    _update_table
)


def get_user(event, context):
    try:
        user_id = _extract_path_param(event, "user_id")
        table = _get_table('users')
        user = _get_user(user_id, table)

        return _success_response(user)

    except ApiError as e:
        return _process_api_error(e)


def create_user(event, context):
    try:
        body = _extract_body(event)
        table = _get_table('users')

        new_id = str(uuid.uuid1())
        table.put_item(
            Item={
                "user_id": new_id,
                "name": body["name"] if "name" in body else None,
                "image_url": body["image_url"] if "image_url" in body else None,
            }
        )

        return _success_response({"user_id": new_id})

    except ApiError as e:
        return _process_api_error(e)


def update_user(event, context):
    try:
        user_id = _extract_path_param(event, "user_id")
        body = _extract_body(event)
        table = _get_table('users')
        _get_user(user_id, table)

        if "name" not in body or "image_url" not in body:
            raise ApiError("Invalid body")

        _update_table(table, user_id, {
            "name": body["name"],
            "image_url": body["image_url"]
        })

        return _success_response()

    except ApiError as e:
        return _process_api_error(e)


def delete_user(event, context):
    try:
        user_id = _extract_path_param(event, "user_id")
        table = _get_table('users')

        table.delete_item(Key={"user_id": user_id})

        return _success_response()

    except ApiError as e:
        return _process_api_error(e)
