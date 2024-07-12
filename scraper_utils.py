import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from dynamic_pybloom import BloomFilter

def find_domain(url):
    domain = urlparse(url).netloc
    return domain

class URLValidator():
    def __init__(self):
        self.url = None
        self.domain = None

    def validate_url(self, url):
        #Check domain return true or false
        url_domain = find_domain(url)
        if str(url_domain) == str(self.domain):
            return True
        return False

class URLFilter():
    def __init__(self, links):
        self.bloom_filter = BloomFilter(capacity=100000, error_rate=0.1)
        self.links = links
    def filter_link(self, links):
        filter = self.bloom_filter
        filtered_links = []
        #check and append to queue
        for link in self.links :
            if not link in filter:
                filter.add(self.link)
                filtered_links.append(link)
        return filtered_links

# class Downloader():
#     def __init__(self, url):
#         validator = URLValidator(url)
#         if validator.validate_url(url):
#             try:
#                 response = requests.get(url)
#                 content = response.text
