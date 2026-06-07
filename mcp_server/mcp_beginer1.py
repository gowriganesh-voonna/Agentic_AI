import sys
import json
import asyncio


async def handle_request(request):

    method = request.get("method")

    if method == "ping":
        return "pong"
    return {"error": f"Method '{method}' not supported"}


async def main():

    loop = asyncio.get_event_loop()

    while True:

        line = await loop.run_in_executor(None, sys.stdin.readline)

        if not line:
            break

        request = json.loads(line)

        response = {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": await handle_request(request),
        }

        print(json.dumps(response))
        sys.stdout.flush()


import requests


def weather_tool(params):
    city = params.get("city", "London")
    url = f"https://wttr.in/{city}?format=3"

    response = requests.get(url)
    return response.text





if __name__ == "__main__":
    print(weather_tool({"city": "New York"}))
    asyncio.run(main())
