"""Validate a local response object, without making an HTTP request."""
import re


def check_response(data):
    if not isinstance(data, dict):
        raise ValueError("Response must be an object")
    status, payload = data.get("status"), data.get("payload")
    if type(status) is not int or status not in (200, 400, 404, 429, 500) or not isinstance(payload, dict):
        raise ValueError("Use a supported status and an object payload")
    if status == 200:
        if set(payload) != {"items", "next_cursor"} or not isinstance(payload["items"], list) or len(payload["items"]) > 100:
            raise ValueError("Page requires items and next_cursor; at most 100 items")
        ids = []
        for item in payload["items"]:
            if not isinstance(item, dict) or set(item) != {"id", "name"}:
                raise ValueError("Each item requires exactly id and name")
            key, name = item["id"], item["name"]
            if type(key) is not int or key < 1 or not isinstance(name, str) or not 1 <= len(name.strip()) <= 100:
                raise ValueError("Invalid listing ID or name")
            ids.append(key)
        if ids != sorted(set(ids)):
            raise ValueError("Items must have unique ascending IDs")
        cursor = payload["next_cursor"]
        if cursor is not None and (type(cursor) is not int or not ids or cursor != ids[-1]):
            raise ValueError("Non-null cursor must equal the last item ID")
        return {"status": status, "kind": "page", "item_count": len(ids), "has_next": cursor is not None}
    if set(payload) != {"error"} or not isinstance(payload["error"], dict) or set(payload["error"]) != {"code", "message"}:
        raise ValueError("Error payload requires code and message")
    code, message = payload["error"]["code"], payload["error"]["message"]
    if not isinstance(code, str) or not re.fullmatch(r"[a-z][a-z0-9_]{0,39}", code):
        raise ValueError("Invalid error code")
    if not isinstance(message, str) or not 1 <= len(message.strip()) <= 200:
        raise ValueError("Error message must contain 1–200 characters")
    return {"status": status, "kind": "error", "code": code}
