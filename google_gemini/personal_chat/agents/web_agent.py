# agents/web_agent.py
from tavily import TavilyClient
from config.settings import TAVILY_API_KEY

# Initialize once using your config key
tavily = TavilyClient(api_key=TAVILY_API_KEY)

def fetch_from_web(query: str) -> str:
    """
    Fetch relevant and summarized information from the web using Tavily API.
    - Tries qna_search() for direct answers.
    - Falls back to search() if qna_search is unavailable.
    - Returns a clean summarized result with 2–3 sources.
    """
    try:
        print(f"🌐 Searching the web for: {query}")

        # Try qna_search first (if supported by your Tavily package version)
        try:
            response = tavily.qna_search(query)
            if response and "answer" in response:
                answer = response["answer"]
                sources = response.get("sources", [])
                source_text = ""

                if sources:
                    links = [s.get("url") for s in sources if "url" in s]
                    if links:
                        source_text = "\n\n🔗 Sources:\n" + "\n".join(links[:3])

                print("✅ Web info fetched via qna_search()")
                return f"{answer}{source_text}"
        except Exception as inner_e:
            print(f"⚠️ qna_search() not available, falling back to .search(): {inner_e}")

        # Fall back to the general search() method
        result = tavily.search(query=query, max_results=3)

        if not result or "results" not in result or len(result["results"]) == 0:
            return "No relevant web information found."

        summaries = []
        for r in result["results"]:
            title = r.get("title", "No title")
            url = r.get("url", "")
            content = r.get("content", "")
            summaries.append(f"🔗 **{title}**\n{content}\n{url}")

        combined = "\n\n".join(summaries[:3])
        print("✅ Web info fetched via search()")
        return f"🌐 Web Results (via Tavily):\n\n{combined}"

    except Exception as e:
        print(f"⚠️ Web fetch error: {e}")
        return f"⚠️ Error fetching from web: {e}"
