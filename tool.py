from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
load_dotenv()

<<<<<<< HEAD
tavily_api_key = os.getenv("TAVILY_API_KEY") or os.getenv("TAVILY_KEY")
tavily = TavilyClient(api_key=tavily_api_key)
=======
tavily=TavilyClient(api_key=os.getenv("TAVILY_KEY"))
>>>>>>> a3e35a63d7a3930343af923c1b88e842743a5533

@tool
def web_search(query: str) -> str:
    """search the web for recent and reliable information on the given topic and returns Titles,URLs and Snippets of the top 5 results."""
<<<<<<< HEAD
    try:
        response = tavily.search(query=query, max_results=5)
        results = response.get('results', [])
        output = ""
        for result in results:
            title = result.get('title', 'No Title')
            url = result.get('url', 'No URL')
            snippet = result.get('content', '')[:1000]
            output += f"Title: {title}\nURL: {url}\nSnippet: {snippet}\n\n"
        return output.strip()
    except Exception as e:
        return f"Error performing search: {e}"
=======
    results = tavily.search(query=query, num_results=5)
    output = ""
    for result in results:
        title = result['title']
        url = result['url']
        snippet = result['snippet']
        output += f"Title: {title}\nURL: {url}\nSnippet: {snippet}[:300]\n\n"
    return output.strip()
    return "\n".join(output)
>>>>>>> a3e35a63d7a3930343af923c1b88e842743a5533

@tool
def web_scrape(url: str) -> str:
    """scrape the content of the given URL and returns the text content of the webpage for better reading."""
    try:
        response = requests.get(url,timeout=7,headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        for symbol in soup(['script', 'style','img','nav','footer']):
            symbol.decompose()
<<<<<<< HEAD
        return soup.get_text(separator=" ", strip=True)[:40000]
=======
        return soup.get_text(separator=" ", strip=True)[:3000]
>>>>>>> a3e35a63d7a3930343af923c1b88e842743a5533
    except requests.exceptions.RequestException as e:
        return f"Error fetching the URL: {e}"