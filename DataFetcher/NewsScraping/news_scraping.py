from langchain_community.document_loaders.firecrawl import FireCrawlLoader
from dotenv import load_dotenv
import os

# load .env file
load_dotenv()
"""
FireCrawl crawls and convert any website into LLM-ready data. 
It crawls all accessible subpages and give you clean markdown and metadata for each. No sitemap required.

FireCrawl handles complex tasks such as reverse proxies, caching, rate limits, and content blocked by JavaScript. 
Built by the mendable.ai team.
"""

API_KEY = os.getenv('FIRECRAWL_API_KEY', '')

"""
FireCrawlLoader is a document loader that uses the FireCrawl API to scrape, crawl, and map URLs.
    Modes
        scrape: Scrape single url and return the markdown.
        crawl: Crawl the url and all accessible sub pages and return the markdown for each one.
        map: Maps the URL and returns a list of semantically related pages.
    Crawl Options
        You can also pass params to the loader. 
        This is a dictionary of options to pass to the crawler. 
        See the FireCrawl API documentation for more information.
API reference
    For detailed documentation of all `FireCrawlLoader` features and configurations head to the API reference: 
    https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.firecrawl.FireCrawlLoader.html
"""

# Scrape mode
loader = FireCrawlLoader(
    api_key=API_KEY,
    url="https://firecrawl.dev",
    mode="scrape",
    params={
        'limit': 100,
        'scrapeOptions': {'formats': ['markdown', 'html']}
    }
)
pages = []
for doc in loader.lazy_load():
    pages.append(doc)

print(pages)

# Crawl mode
loader = FireCrawlLoader(
    api_key=API_KEY,
    url="https://firecrawl.dev",
    mode="crawl",
)
data = loader.load()
print(pages[0].page_content[:100])
print(pages[0].metadata)

# Map mode
loader = FireCrawlLoader(
    api_key=API_KEY,
    url="https://firecrawl.dev",
    mode="map"
)
docs = loader.load()
print(docs)

