from scraper_utils import URLFilter, URLValidator
from scraper_utils import find_domain
from celery_tasks import download_content
import sys

class Scraper():
    def __init__(self):
        self.start_url = self.get_start_url()
        self.page_limit = 100
        self.domain = find_domain(self.start_url)
        self.export_file_name = str(self.domain)

    def get_start_url(self):
        return sys.argv[1]

    def set_page_limit(self):
        self.page_limit = sys.argv[2]

    def start_crawl(self):
        #Initiate the crawling process
        validator = URLValidator()
        # valid_start_url = validator.validate_url(self.start_url)
        valid_start_url = self.start_url
        if valid_start_url:
            print(f"Crawl has started for URL : {self.start_url}")
            download_content.apply_async(
                args=[self.start_url]
            )
        else:
            print("Invalid start URL. Please check the URL and try again.")

demo_scraper = Scraper()
demo_scraper.start_crawl()
