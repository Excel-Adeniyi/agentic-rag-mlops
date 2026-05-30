import requests
from bs4 import BeautifulSoup
import os
import time


docs_to_scrape = [
    {
        "url": "https://docs.docker.com/get-started/docker-overview/",
        "filename": "docs/docker_overview.md"
    },
    {
        "url": "https://docs.docker.com/engine/containers/run/",
        "filename": "docs/docker_run.md"
    },
    {
        "url": "https://docs.docker.com/compose/intro/features-uses/",
        "filename": "docs/docker_compose.md"
    },
    {
         "url": "https://docs.docker.com/engine/network/",
        "filename": "docs/docker-networking.md"
    },
    {
        "url": "https://www.jenkins.io/doc/book/pipeline/syntax/",
        "filename": "docs/jenkins-pipeline-syntax.md"
    },
    {
        "url": "https://www.jenkins.io/doc/book/pipeline/getting-started/",
        "filename": "docs/jenkins-pipeline-getting-started.md"
    },
    {
        "url": "https://www.jenkins.io/doc/book/managing/",
        "filename": "docs/jenkins-managing.md"
    }
    ]

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

def scrape_page(url):
    """Fetch a page and extract clean text content"""
    response = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Remove navigation, headers, footers, scripts and styles
    for tag in soup(['nav', 'header', 'footer', 'script', 
                     'style', 'aside', 'form']):
        tag.decompose()
    for tag in soup.find_all('div', class_='sidebar-nav'):
        tag.decompose()
    # Try to find the main content area
    main = (soup.find('div', class_='ctc') or soup.find('main') or 
            soup.find('article') or 
            soup.find('div', class_='content') or
            soup.find('div', class_='documentation') or
            soup.body)
    
    if main:
        # Get clean text with newlines preserved
        lines = []
        for element in main.find_all(['h1', 'h2', 'h3', 'h4', 'p', 
                                       'li', 'code', 'pre']):
            text = element.get_text(strip=True)
            if text and len(text) > 10:
                if element.name in ['h1', 'h2', 'h3', 'h4']:
                    lines.append(f"\n## {text}\n")
                elif element.name in ['code', 'pre']:
                    lines.append(f"`{text}`")
                else:
                    lines.append(text)
        return '\n'.join(lines)
    return ""

# Scrape each page
for doc in docs_to_scrape:
    try:
        print(f"Scraping {doc['url']}...")
        content = scrape_page(doc['url'])
        
        if len(content) < 500:
            print(f"  Warning: only {len(content)} chars, may be blocked")
        else:
            with open(doc['filename'], 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Saved {doc['filename']} ({len(content)} characters)")
        
        time.sleep(2)  # Be polite, wait between requests
        
    except Exception as e:
        print(f"  Failed {doc['filename']}: {e}")

print("\nDone. Check docs/ folder.")
