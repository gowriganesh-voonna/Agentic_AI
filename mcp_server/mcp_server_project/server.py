import sys
import json
from tools import Tools


def list_tools():

    return [
        {"name": "add_tool", "description": "Add two numbers."},
        {
            "name": "file_reader_tool",
            "description": "Read a file path and return its content.",
        },
        {
            "name": "system_info_tool",
            "description": "Get current working directory and list of files in the current directory.",
        },
    ]


def handle_request(request):

    method = request.get("method")

    if method == "list_tools":
        return list_tools()

    if method == "call_tool":

        params = request.get("params", {})

        name = params.get("name")

        args = params.get("args", {})

        if name in Tools:
            try:

                return Tools[name](args)
            except Exception as e:
                return f"Error calling tool {name}: {str(e)}"

        return "Tool not found"

    return "Unknown Method"


while True:

    line = sys.stdin.readline()

    if not line:
        break

    request = json.loads(line)

    response = {
        "jsonrpc": "2.0",
        "id": request.get("id"),
        "result": handle_request(request),
    }

    print(json.dumps(response))
    sys.stdout.flush()
