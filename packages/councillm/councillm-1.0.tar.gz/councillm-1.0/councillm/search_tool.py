from ddgs import DDGS

def web_search(query: str, max_results: int = 5) -> str:
    snippets = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            title = r.get("title", "")
            body = r.get("body", "")
            url = r.get("href", "")
            snippets.append(f"- {title}: {body} ({url})")

    return "\n".join(snippets)
