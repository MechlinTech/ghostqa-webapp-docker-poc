import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import pandas as pd
from utils.TrueTest.Data import UserJourneyGraph


def generate_input_text(input_type, placeholder):
    if 'email' in input_type:
        return 'example@example.com'
    elif 'password' in input_type:
        return 'securepassword123'
    elif 'search' in input_type:
        return 'search query'
    elif 'tel' in input_type:
        return '1234567890'
    elif 'number' in input_type:
        return '123'
    elif 'date' in input_type:
        return '2024-03-19'
    elif 'time' in input_type:
        return '12:00 PM'
    elif 'url' in input_type:
        return 'http://example.com'
    elif 'text' in input_type:
        return placeholder
    else:
        return ''
    
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
    
def get_interactable_elements(url, domain):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    elements = []

    # Find clickable elements (links and buttons)
    for link in soup.find_all(['a', 'button']):
        href = link.get('href')
        if href:
            absolute_link = urljoin(url, href)
            parsed_link = urlparse(absolute_link)
            if parsed_link.netloc == domain:
                elements.append({'interaction_type': 'Clickable_Link', 'source_url':url,'destination_url': absolute_link,"text":link.string})

    # Find input fields
    for input_field in soup.find_all('input'):
        input_type = input_field.get('type')
        if input_type != 'hidden':
            placeholder = input_field.get('placeholder', '')
            input_text = generate_input_text(input_type, placeholder)
            elements.append({'interaction_type': 'Input Field', 'Name': input_field.get('name'), 'Placeholder': placeholder, 'Input Text': input_text, 'source_url': url})

    return elements

def crawl_website(start_url, max_depth=3):
    parsed_start_url = urlparse(start_url)
    domain = parsed_start_url.netloc
    visited = set()
    user_journey = UserJourneyGraph(start_url)

    def crawl(url, depth,journey = []):
        if depth > max_depth:
            return
        if url in visited:
            return
        visited.add(url)

        interactable_elements = get_interactable_elements(url, domain)
        for element in interactable_elements:
            user_journey.add_interaction(**element)

        links = get_links(url, domain)
        for link in links:
            absolute_link = urljoin(url, link)
            if start_url != absolute_link:
                crawl(absolute_link, depth + 1)
            else: 
                PASS= True
                break
        
        return user_journey
    user_journey = crawl(start_url, 1,[])

    return user_journey

start_url = "https://mechlintech.com/"
user_journey = crawl_website(start_url)


user_journey.visualize_graph()

