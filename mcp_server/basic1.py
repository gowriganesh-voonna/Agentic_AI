import sys
import json


while True:

    line = sys.stdin.readline()

    if not line:
        break

    request = json.loads(line)

    method = request.get("method")

    if method == "greet":

        result = "Hello i am greet method"

    elif method == "add":

        params = request.get("params", {})

        result = params.get("a", 0) + params.get("b", 0)

    else:
        result = f"Unknown method: {method}"

    response = {"jsonrpc": "2.0", "id": request.get("id"), "result": result}

    print(json.dumps(response))

    sys.stdout.flush()
