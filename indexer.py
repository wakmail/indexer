import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from collections import deque

def normalize_url(url):
    # Check if the URL has http:// or https:// prefix
    if not url.startswith('http://') and not url.startswith('https://'):
        # Add the appropriate prefix based on the original URL
        url = 'http://' + url
    
    return url

def website_crawler(start_url, max_pages):
    start_url = normalize_url(start_url)  # Normalize the input URL
    visited = set()  # Set to store visited URLs
    queue = deque([(start_url, 0)])  # Queue to store URLs to be crawled
    index = {}  # Dictionary to store indexed URLs

    while queue and len(visited) < max_pages:
        url, depth = queue.popleft()
        
        if url in visited:
            continue
        
        # Send a GET request to the URL
        response = requests.get(url)
        
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract information from the parsed HTML
            links = soup.find_all('a')
            
            # Process the extracted links
            for link in links:
                href = link.get('href')
                if href:
                    # Check if the URL has http:// or https:// prefix
                    if not href.startswith('http://') and not href.startswith('https://'):
                        # Add the appropriate prefix based on the original URL
                        href = urljoin(url, href)
                    
                    # Add the URL to the index
                    if href not in index:
                        index[href] = depth + 1
                    
                    # Enqueue the URL for crawling if it hasn't been visited
                    if href not in visited and depth + 1 < max_pages:
                        queue.append((href, depth + 1))
        
        # Mark the current URL as visited
        visited.add(url)
    
    return index

# Example usage
start_url = input("Enter a URL: ")
max_pages = 50
index = website_crawler(start_url, max_pages)

# Print the indexed URLs
for url, depth in index.items():
    print(f"URL: {url}, Depth: {depth}")
  

