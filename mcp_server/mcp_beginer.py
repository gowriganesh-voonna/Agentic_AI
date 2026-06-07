import sys
import json


def add_tool(param):
    return param.get("a", 0) + param.get("b", 0)


def greet_tool(param):
    return f"Hello, {param.get('name','user')}!"


Tools = {"add": add_tool, "greet": greet_tool}


def list_tools():
    return [
        {
            "name": "add",
            "description": "Adds two numbers. Parameters: a (number), b (number)",
        },
        {"name": "greet", "description": "Greets a person. Parameters: name (string)"},
    ]


def handle_request(request):

    method = request.get("method")
    params = request.get("params", {})

    if method == "list_tools":
        return list_tools()

    if method == "call_tool":

        name = params.get("name")
        tool_params = params.get("params", {})
        args = tool_params.get("arguments", {})

        if name in Tools:

            return Tools[name](args)

        return {"error": f"Tool '{name}' not found"}

    return {"error": f"Method '{method}' not supported"}


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
