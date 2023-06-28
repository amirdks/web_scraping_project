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

init_url = "https://www.e-estekhdam.com/search/%D8%A7%D8%B3%D8%AA%D8%AE%D8%AF%D8%A7%D9%85-%D8%AF%D8%B1-%D8%A7%D9%84%D8%A8%D8%B1%D8%B2"


class EEstekhdam(Jobs):
    def __init__(self, url=init_url, item_count=70, page_item_number=20):
        super(EEstekhdam, self).__init__(url, item_count, page_item_number)
        self.base_url = "https://www.e-estekhdam.com"
        self.site_id = Site.objects.get(title="e_estekhdam").id

    def get_page_result(self):
        page_results = []
        for page in self.rang:
            try:
                response = requests.get(
                    self.url + f"?page={page}" if page != 1 else self.url,
                    headers={"User-Agent": "Mozilla/5.0"}
                )
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                raise self.RequestException(e)
            soup = BeautifulSoup(response.content, "html.parser")
            result = soup.find_all("div", {
                "class": "job-list-item"})
            page_results.append(result)
        return page_results

    def get_job_results(self, page_results):

        for page in page_results:
            for item in page[::-1]:
                link_element = item.find("a", {"class": "media"})
                link = self.base_url + link_element.get("href")
                title_element = item.find("div", {"class": "title"})
                title = title_element.find("span").text.strip()
                image = item.find("img")
                image_link = None
                if image:
                    image_link = self.base_url + image.get("src")
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
