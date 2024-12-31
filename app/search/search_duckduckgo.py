import requests
from bs4 import BeautifulSoup
from app.config import QUERY, MAX_RESULTS

def search_duckduckgo(query=QUERY, exclude_urls=[], max_results=MAX_RESULTS):
    base_url = "https://duckduckgo.com/html/"
    params = {"q": query}
    headers = {"User-Agent": "Mozilla/5.0"}

    results = []
    response = requests.get(base_url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    for link in soup.find_all("a", href=True):
        url = link["href"]
        if "http" in url and url not in exclude_urls:
            results.append({"url": url, "query": query})
        if len(results) >= max_results:
            break
    return results
