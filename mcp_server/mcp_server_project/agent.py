import subprocess
import json


def call_server(request):

    process = subprocess.Popen(
        ["python", "server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )

    process.stdin.write(json.dumps(request) + "\n")
    process.stdin.flush()

    response = process.stdout.readline()

    return json.loads(response)


def agent(user_input):

    if "add" in user_input:

        return call_server(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "call_tool",
                "params": {"name": "add_tool", "args": {"a": 5, "b": 10}},
            }
        )

    elif "files" in user_input:
        return call_server(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "call_tool",
                "params": {"name": "system_info_tool", "args": {}},
            }
        )

    return {"response": "I don't understand the request."}


while True:

    user_input = input("Enter your request: ")

    if user_input.lower() in ["exit", "quit"]:
        break

    response = agent(user_input)

    print("Response:", response)
