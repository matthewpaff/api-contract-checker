"""Original mock API payloads with independently specified validation outcomes."""


def make_case(index):
    key, kind = index * 10 + 1, index % 10
    items = [{"id": key, "name": "Cafe {}".format(index)}, {"id": key + 1, "name": "Shop {}".format(index)}]
    data = {"status": 200, "payload": {"items": items, "next_cursor": None}}
    if kind == 0:
        data["status"] = True
        description = "reject boolean response status values"
    elif kind == 1:
        data["payload"]["items"] = [items[0], dict(items[0])]
        description = "reject duplicate page item IDs"
    elif kind == 2:
        data["payload"]["next_cursor"] = key + 100
        description = "reject cursors that differ from the last item ID"
    elif kind == 3:
        data["payload"]["items"][0]["name"] = "   "
        description = "reject blank listing names"
    elif kind == 4:
        data = {"status": 400, "payload": {"error": {"code": "Bad Code", "message": "Invalid request"}}}
        description = "reject malformed structured error codes"
    elif kind in (5, 6):
        status, code = (404, "not_found") if kind == 5 else (429, "rate_limited")
        data = {"status": status, "payload": {"error": {"code": code, "message": "Mock error {}".format(index)}}}
        expected = {"status": status, "kind": "error", "code": code}
        description = "accept a structured {} response".format(status)
    elif kind == 7:
        data["payload"]["items"] = []
        expected = {"status": 200, "kind": "page", "item_count": 0, "has_next": False}
        description = "accept an empty terminal result page"
    else:
        data["payload"]["next_cursor"] = key + 1 if kind == 8 else None
        expected = {"status": 200, "kind": "page", "item_count": 2, "has_next": kind == 8}
        description = "validate an ordered page with {} cursor".format("a continuation" if kind == 8 else "no continuation")
    result = {"id": "contracts-{:04d}".format(index), "description": description, "input": data}
    result.update({"expected_error": True} if kind < 5 else {"expected": expected})
    return result
