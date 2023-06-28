import datetime
import time
from urllib.parse import urlsplit

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from main_module.models import Site
from main_module.sites.Jobs import Jobs
from selenium.webdriver.firefox.options import Options

init_url = "https://jobvision.ir/jobs?sort=0"


class JobVision(Jobs):
    def __init__(self, url=init_url, item_count=25, page_item_number=30):
        super(JobVision, self).__init__(url, item_count, page_item_number)
        # self.image_regex = r'https?:\/\/storage.jobinjacdn.com/other/files/uploads/images/[\s\S]*'
        self.base_url = "https://jobvision.ir"
        self.site_id = Site.objects.get(title="jobvision").id
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1080")
        # self.driver = webdriver.Firefox(options=options)
        self.driver = webdriver.Chrome(options=options)
        # self.driver = webdriver.Remote("http://selenium:4444/wd/hub", DesiredCapabilities.FIREFOX, options=options)
        # self.rang = self.range1(1, self.page_count)

    def get_page_result(self):
        page_results = []
        for index, page in enumerate(self.rang):
            self.driver.get(init_url)
            time.sleep(5)
            self.scroll_down()
            elements = self.driver.find_elements_by_class_name("desktop-job-card")
            page_results.append(elements)
        return page_results

    def get_job_results(self, page_results):
        for page in page_results:
            for item in page[::-1]:
                link_element = item.get_attribute("href")
                link_obj = urlsplit(link_element)
                link = f"{link_obj.scheme}://{link_obj.netloc}{link_obj.path}"
                date = datetime.datetime.now()
                image_link = item.find_element_by_css_selector(".company-brand.company-logo").get_attribute("src")
                title = item.find_element_by_css_selector(
                    "div.job-card-title.w-100.font-weight-bolder.text-black.px-0.pl-4").text
                self.links_list.append(link)
                result = {
                    "title": title,
                    "published_at": date,
                    "image": image_link,
                    "link": link,
                    "site_id": self.site_id
                }
                self.job_results.append(result)