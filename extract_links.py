# Import required libraries and custom modules
from bs4 import BeautifulSoup

def get_urls(email_body):
    urls = []
    # Check if the email in HTML format
    if '<html' in email_body.lower():
        # Parse the HTML
        soup = BeautifulSoup(email_body, 'html.parser')
        # Find all links
        found_links = soup.find_all('a')
        for link in found_links:
            # Extract and add to the list
            urls.append(link.get('href'))
        return urls
    else:
        return None

