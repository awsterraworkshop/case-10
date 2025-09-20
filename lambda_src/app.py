import json
import os

def _resp(status=200, body=None, headers=None):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json", **(headers or {})},
        "body": json.dumps(body if body is not None else {})
    }

def handler(event, context):
    # Demonstrate what we receive
    route = f"{event.get('httpMethod','GET')} {event.get('path','/')}"
    qs    = event.get("queryStringParameters") or {}
    pathp = event.get("pathParameters") or {}
    body  = event.get("body")
    try:
        jbody = json.loads(body) if body else None
    except Exception:
        jbody = None

    # Simple router based on path
    path = event.get("path","/")
    method = event.get("httpMethod","GET").upper()

    if path.startswith("/items/") and method == "GET":
        item_id = pathp.get("id")
        return _resp(200, {
            "ok": True,
            "action": "get_item",
            "id": item_id,
            "query": qs
        })

    if path == "/items" and method == "POST":
        return _resp(201, {
            "ok": True,
            "action": "create_item",
            "data": jbody or {},
        })

    if path == "/search" and method == "GET":
        tag   = qs.get("tag")
        limit = int(qs.get("limit", 10))
        return _resp(200, {
            "ok": True,
            "action": "search",
            "tag": tag,
            "limit": limit
        })

    # Default: echo request for learning
    return _resp(200, {
        "service": os.getenv("SERVICE_NAME","svc"),
        "route": route,
        "pathParameters": pathp,
        "queryStringParameters": qs,
        "body": jbody
    })
