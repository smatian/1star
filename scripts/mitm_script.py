from mitmproxy import http
import json

def response(flow: http.HTTPFlow) -> None:
    if "application/json" in flow.response.headers.get("content-type", ""):
        data = json.loads(flow.response.content)
        data["test"] = "Hello, World"
        flow.response.text = json.dumps(data)
