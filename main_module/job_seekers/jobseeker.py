import datetime
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.firefox.options import Options

from main_module.models import JobSeeker, Site
from main_module.sites.Jobs import Jobs

init_url = 'https://daneshmandjobs.com/candidates/'


# class JobSeekerClass(Jobs):
#     def __init__(self, url=init_url, item_count=50, page_item_number=12):
#         super(JobSeekerClass, self).__init__(url, item_count, page_item_number)
#         self.image_regex = r'https?:\/\/storage.jobinjacdn.com/other/files/uploads/images/[\s\S]*'
#         self.base_url = "https://daneshmandjobs.com"
#         self.site_id = Site.objects.get(title="jobseeker").id
#
#     def save_jobs_in_db(self):
#         print("salam")
#         duplicated_job_items = JobSeeker.objects.filter(site_id=self.site_id, link__in=self.links_list).values_list(
#             "link")
#         duplicated = [link[0] for link in duplicated_job_items]
#         print("duplicated==> ", duplicated)
#         print("len==>", len(self.job_results))
#         print("dup len==>", len(duplicated))
#         res = [x for x in self.job_results if x["link"] not in duplicated]
#         print("job results==> ", self.job_results)
#         for salam in self.job_results:
#             print("job link==>", salam.get("link"))
#             print("job full name==>", salam.get("full_name"))
#         print("res ==> ", res)
#         for idx, item in enumerate(res[::-1]):
#             # if self.get_last_job_link() == item["link"]:
#             #     return "almost_success"
#             if idx == 0: item.update({"is_last": True})
#             print("raft bara save")
#             JobSeeker.objects.create(**item)
#         return "success"
#
#     def get_page_result(self):
#         page_results = []
#         for page in self.rang:
#             try:
#                 response = requests.get(
#                     self.url + f"?page={page}" if page != 1 else self.url,
#                     headers={"User-Agent": "Mozilla/5.0"}
#                 )
#             except requests.exceptions.RequestException as e:  # This is the correct syntax
#                 raise self.RequestException(e)
#             soup = BeautifulSoup(response.content, "html.parser")
#             result = (
#                 soup.findAll("div", attrs={"class": "candidate-item"})[
#                 :self.last_page_item]
#                 if len(self.rang) == page
#                 else soup.findAll("div", attrs={"class": "candidate-item"})
#             )
#             page_results.append(result)
#         return page_results
#
#     def get_job_results(self, page_results):
#
#         for page in page_results:
#             for item in page[::-1]:
#                 link_element = item.find("a")
#                 link = link_element.get("href")
#                 full_name = item.find("img").get("alt").strip()
#                 # time = item.find("span", class_="kt-post-card__bottom-description kt-text-truncate").text.strip()
#                 # instantaneous = item.find("span", class_="kt-post-card__red-text")
#                 # if instantaneous:
#                 #     time = "instantaneous"
#                 image = item.find("img")
#                 image_link = None
#                 if image:
#                     image_link = image.get("data-lazy-src")
#                 date = datetime.datetime.now()
#                 self.links_list.append(link)
#                 result = {
#                     "full_name": full_name,
#                     "image": image_link,
#                     "link": link,
#                     "site_id": self.site_id
#                 }
#                 self.job_results.append(result)
class JobSeekerClass(Jobs):
    def range1(self, start, end):
        return range(start, end + 1)

    def __init__(self, url=init_url, item_count=24, page_item_number=12):
        super(JobSeekerClass, self).__init__(url, item_count, page_item_number)
        self.image_regex = r'https?:\/\/storage.jobinjacdn.com/other/files/uploads/images/[\s\S]*'
        self.base_url = "https://daneshmandjobs.com"
        self.site_id = Site.objects.get(title="jobseeker").id
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1080")
        # self.driver = webdriver.Firefox(options=options)
        self.driver = webdriver.Chrome(options=options)
        self.rang = self.range1(1, self.page_count)

    def save_jobs_in_db(self):
        duplicated_job_items = JobSeeker.objects.filter(site_id=self.site_id, link__in=self.links_list).values_list(
            "link")
        duplicated = [link[0] for link in duplicated_job_items]
        res = [x for x in self.job_results if x["link"] not in duplicated]
        new_list = []
        link_list = []
        for item in res:
            if not item.get("link") in link_list:
                new_list.append(item)
            link_list.append(item.get("link"))
        for idx, item in enumerate(new_list[::-1]):
            if idx == 0: item.update({"is_last": True})
            JobSeeker.objects.create(**item)
        return "success"

    def get_page_result(self):
        page_results = []
        for index, page in enumerate(self.rang):
            if index == 0:
                self.driver.get(init_url)
                time.sleep(2)
                self.scroll_down()
            else:
                try:
                    next_page_element = self.driver.find_element_by_css_selector(
                        f'a[href="https://daneshmandjobs.com/candidates/page/{page}/"]')
                except NoSuchElementException as e:
                    next_page_element = self.driver.find_element_by_css_selector(
                        f'a[href="https://daneshmandjobs.com/wp-admin/admin-ajax.php?paged={page}"]')
                next_page_element.click()
                time.sleep(25)
                self.scroll_down()
            company_page = self.driver.page_source
            linkedin_soup = BeautifulSoup(company_page.encode("utf-8"), "html.parser")
            linkedin_soup.prettify()
            test_results = linkedin_soup.find_all("div", {"class": "candidate-item"})
            page_results.append(test_results)
        return page_results

    def get_job_results(self, page_results):

        for page in page_results:
            for item in page[::-1]:
                link_element = item.select_one("h3.candidate-title a")
                if not link_element:
                    link = item.select_one("a.view-candidate").get("href")
                    full_name = item.select_one("div.candidate-headline").text.strip()
                else:
                    full_name = link_element.text.strip()
                    link = link_element.get("href")
                description = item.select_one("div.categories")
                if not description:
                    description = item.select_one("div.desc")
                description = description.text.strip()
                image = item.select_one("img")
                image_link = None
                if image:
                    image_link = image.get("data-lazy-src")
                    if not image_link:
                        image_link = image.get("src")
                date = datetime.datetime.now()
                self.links_list.append(link)
                result = {
                    "full_name": full_name,
                    "image": image_link,
                    "link": link,
                    "site_id": self.site_id,
                    "description": description,
                }
                self.job_results.append(result)
