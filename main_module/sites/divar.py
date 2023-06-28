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

init_url = "https://divar.ir/s/karaj/jobs/"


class Divar(Jobs):
    def __init__(self, url=init_url, item_count=32, page_item_number=24):
        super(Divar, self).__init__(url, item_count, page_item_number)
        self.image_regex = r'https?:\/\/storage.jobinjacdn.com/other/files/uploads/images/[\s\S]*'
        self.base_url = "https://divar.ir"
        self.site_id = Site.objects.get(title="divar").id

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
            result = (
                soup.findAll("div", attrs={"class": "post-card-item-af972 kt-col-6-bee95 kt-col-xxl-4-e9d46"})[
                :self.last_page_item]
                if len(self.rang) == page
                else soup.findAll("div", attrs={"class": "post-card-item-af972 kt-col-6-bee95 kt-col-xxl-4-e9d46"})
            )
            page_results.append(result)
        return page_results

    def get_job_results(self, page_results):

        for page in page_results:
            for item in page[::-1]:
                link_element = item.find("a")
                link = self.base_url + link_element.get("href")
                title = item.find("h2", class_="kt-post-card__title").text.strip()
                time = item.find("span", class_="kt-post-card__bottom-description kt-text-truncate").text.strip()
                instantaneous = item.find("span", class_="kt-post-card__red-text")
                if instantaneous:
                    time = "instantaneous"
                image = item.find("img")
                image_link = None
                if image:
                    image_link = image.get("data-src")
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
