import sys
import json


while True:

    line = sys.stdin.readline()

    if not line:
        break

    request = json.loads(line)

    response = {"jsonrpc": "2.0", "id": request.get("id"), "result": "Hello MCP Server"}

    print(json.dumps(response))

    sys.stdout.flush()

