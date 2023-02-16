import time
import requests
from bs4 import BeautifulSoup

# Set the URL to scrape
url = 'https://www.example.com'

# Set headers to mimic a browser visit
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

try:
    # Send a GET request to the URL
    response = requests.get(url, headers=headers)

    # Raise an HTTPError if status code is >= 400
    response.raise_for_status()

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract relevant data using BeautifulSoup methods
    title = soup.title.string
    links = [link.get('href') for link in soup.find_all('a')]
    paragraphs = [p.text for p in soup.find_all('p')]

    # Store the scraped data in a file
    with open('scraped_data.txt', 'w') as f:
        f.write(f'Title: {title}\n')
        f.write('Links:\n')
        for link in links:
            f.write(f'{link}\n')
        f.write('Paragraphs:\n')
        for paragraph in paragraphs:
            f.write(f'{paragraph}\n')

    print('Scraping completed successfully.')

except requests.exceptions.RequestException as err:
    # Handle errors with try-except blocks and log error messages
    if isinstance(err, requests.exceptions.HTTPError):
        print(f"HTTP Error: {err}")
    elif isinstance(err, requests.exceptions.ConnectionError):
        print(f"Error Connecting: {err}")
    elif isinstance(err, requests.exceptions.Timeout):
        print(f"Timeout Error: {err}")
    else:
        print(f"Something went wrong: {err}")

    # Retry failed requests with an exponential backoff algorithm
    retries = 0
    while retries < 3:
        print(f"Retrying in {2**retries} seconds...")
        time.sleep(2**retries)
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.title.string
            links = [link.get('href') for link in soup.find_all('a')]
            paragraphs = [p.text for p in soup.find_all('p')]
            with open('scraped_data.txt', 'a') as f:
                f.write('Retried Data:\n')
                f.write(f'Title: {title}\n')
                f.write('Links:\n')
                for link in links:
                    f.write(f'{link}\n')
                f.write('Paragraphs:\n')
                for paragraph in paragraphs:
                    f.write(f'{paragraph}\n')
            print('Scraping completed successfully after retries.')
            break
        except requests.exceptions.RequestException as err:
            retries += 1
            if retries == 3:
                print(f"Failed after retries: {err}")
