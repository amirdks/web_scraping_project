import datetime
import re
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options
from main_module.models import Site
from main_module.sites.Jobs import Jobs

init_url = "https://www.irantalent.com/jobs/jobs-in-alborz?sortBy=lived_at&language=persian"


class Irantalent(Jobs):
    def __init__(self, url=init_url, item_count=70, page_item_number=30):
        super(Irantalent, self).__init__(url, item_count, page_item_number)
        self.base_url = "https://www.irantalent.com"
        self.site_id = Site.objects.get(title="irantalent").id

    def get_page_result(self):
        # print("salam")
        page_results = []
        for page in self.rang:
            try:
                response = requests.get(
                    self.url + f"&page={page}" if page != 1 else self.url,
                    headers={"User-Agent": "Mozilla/5.0"}
                )
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                raise self.RequestException(e)
            soup = BeautifulSoup(response.content, "html.parser")
            result = soup.find_all("a", {
                "class": "result-item"})
            page_results.append(result)
        return page_results

    def get_job_results(self, page_results):

        for page in page_results:
            for item in page[::-1]:
                link = self.base_url + item.get("href")
                title = item.find("p", class_="position-title").text.strip()
                image = item.find("img")
                image_link = None
                if image:
                    image_link = image.get("src")
                if image_link == "/assets/css/images/employer-no-logo.png":
                    image_link = self.base_url + image_link
                date = datetime.datetime.now()
                self.links_list.append(link)
                result = {
                    "title": title,
                    "published_at": date,
                    "image": image_link,
                    "link": link,
                    "site_id": self.site_id
                }
                self.job_results.append(result)