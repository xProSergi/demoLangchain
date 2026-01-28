from langchain_community.tools import DuckDuckGoSearchRun

_search = DuckDuckGoSearchRun()

def search(query: str) -> str:
    return _search.run(query)
