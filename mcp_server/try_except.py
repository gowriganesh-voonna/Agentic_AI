import sys
import json

while True:

    line = sys.stdin.readline()

    if not line:
        break

    try:
        request = json.loads(line)

        response = {"jsonrpc": "2.0", "id": request.get("id"), "result": "Sucess"}

    except Exception as e:

        response = {"jsonrpc": "2.0", "id": None, "error": str(e)}

    print(json.dumps(response))
    sys.stdout.flush()
