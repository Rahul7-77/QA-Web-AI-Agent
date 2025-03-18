import requests
from bs4 import BeautifulSoup
from utils.helper import is_valid_url, normalize_url
from urllib.parse import urlparse
import time

def scrape_web(start_url, max_depth=3, max_pages=12):
    """
    Applies BFS traversal (Breadth-first search).
    Recursively scrap website content. Filters out navigation elements, headers, footers.
    Returns list of (text, url) tuples.
    """
    visited_pages = set()
    to_visit = [(start_url, 0)]  # queue structure -> (start_url, depth_of_url)
    contents = []

    headers = {'User-Agent':'Mozilla/5.0'} # Avoids bot detection -> found this in stackoverflow

    while to_visit and len(visited_pages)<max_pages:
        # BFS Traversal
        url, depth = to_visit.pop(0)

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')

            # Filters out nav elements, headers, footers
            for element in soup.select('nav, header, footer, .nav, .footer, script, style'):
                element.decompose()

            text_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4' , 'h5' ,'h6', 'li', 'td', 'th'])
            text = " ".join([element.get_text().strip() for element in text_elements if element.get_text().strip()]) 

            if text:
                contents.append((text, url))

            if depth < max_depth:
                for link in soup.find_all('a', href=True):
                    child_url = normalize_url(url,link['href'])
                    if urlparse(child_url).netloc == urlparse(start_url).netloc: # checks if both parent url and child url are having same domain
                        if child_url not in visited_pages and is_valid_url(child_url) and depth+1 <= max_pages:
                            to_visit.append((child_url, depth+1))
                            visited_pages.add(child_url)
            
            time.sleep(1)
        except requests.RequestException as e:
            print(f"Network error at {url}: {e}")
            continue
    
    return contents if contents else [("No content found in URL.", start_url)]

