import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import pandas as pd

START_URL = "https://mechlintech.com/"

def get_links(url, domain):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            absolute_link = urljoin(url, href)
            parsed_link = urlparse(absolute_link)
            if parsed_link.netloc == domain:
                links.append(absolute_link)
    return links

def crawl_website(start_url, max_depth=10):
    parsed_start_url = urlparse(start_url)
    domain = parsed_start_url.netloc
    visited = set()
    user_journeys = []

    def crawl(url, depth, journey):
        if depth > max_depth:
            return
        if url in visited:
            return
        visited.add(url)

        journey.append(url)
        links = get_links(url, domain)
        PASS = False
        for link in links:
            if START_URL != link:
                crawl(link, depth + 1, journey.copy())
            else: 
                PASS= True
                break

        if depth == max_depth or PASS:
            user_journeys.append(journey)
            df = pd.DataFrame({'User Journeys': user_journeys})

            # Save DataFrame to a CSV file
            df.to_csv('user_journeys.csv', index=False)

    crawl(start_url, 1, [])

    return user_journeys

# start_url = input("Enter the website URL: ")
user_journeys = crawl_website("https://mechlintech.com/")
print("Possible User Journeys:")
for journey in user_journeys:
    print(" -> ".join(journey))
