from tavily import TavilyClient
import os

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_SEARCH_API"))

response = tavily_client.crawl(
    url="https://docs.tavily.com",
    max_depth=3,
    max_breadth=30,
    limit=100,
    select_paths=["/documentation/.*", "/sdk/.*"],
    exclude_paths=["/private/.*", "/admin/.*"],
    allow_external=False,
    extract_depth="advanced",
    include_images=False
)

for page in response["results"]:
    print(page["url"])
    print(page["raw_content"][:200], "...")