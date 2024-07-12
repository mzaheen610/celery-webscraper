from celery import Celery
from bs4 import BeautifulSoup
import requests
from scraper_utils import URLFilter, URLValidator

app = Celery('tasks', broker="amqp://localhost:5672//", backend="rpc://")

@app.task
def download_content(url):
    validator = URLValidator()
    if validator.validate_url(url):
        try:
            response = requests.get(url)
            content = response.text
            extract_tags.apply_async(
                args=[content],
                )
        except:
            print(f"Request failed for URL : {url}")

@app.task
def extract_tags(html_content):
    result = {}
    soup = BeautifulSoup(html_content, 'html.parser')
    result["h1"] = soup.find_all("h1")
    result["h2"] = soup.find_all("h2")
    result["title"] = soup.find_all("title")
    save_results.apply_async(
        args=[result],
    )
    links = soup.find_all("links")
    push_urls_to_queue.apply_async(
        args=[links],
    )

@app.task
def push_urls_to_queue(links):
    url_filter = URLFilter(links)
    unique_urls = url_filter.filter_link()
    for url in unique_urls:
        download_content.apply_async(
            args=[url],
            )

@app.task
def save_results(result):
    with open('output.txt', "a") as file:
        file.write(str(result) + "\n")
    print("Results are saved")
