import datetime
import math
import re
import time

import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

from main_module.models import Job, Site


class Jobs:
    def __init__(self, url, item_count, page_item_number):
        self.url = url
        self.item_count = item_count
        self.page_count = math.ceil(item_count / page_item_number)
        self.last_page_item = item_count % page_item_number
        self.rang = range(self.page_count, 0, -1)
        self.job_results = []
        self.site_id = None
        self.links_list = []

    def save_jobs_in_db(self):
        duplicated_job_items = Job.objects.filter(site_id=self.site_id, link__in=self.links_list).values_list("link")
        duplicated = [link[0] for link in duplicated_job_items]
        res = [x for x in self.job_results if x["link"] not in duplicated]
        new_list = []
        link_list = []
        for item in res:
            if not item.get("link") in link_list:
                new_list.append(item)
            link_list.append(item.get("link"))
        for idx, item in enumerate(new_list[::-1]):
            # if self.get_last_job_link() == item["link"]:
            #     return "almost_success"
            if idx == 0: item.update({"is_last": True})
            Job.objects.create(**item)
        return "success"

    def get_job_detail_soup(self, job):
        try:
            response = requests.get(job.get("link"), headers={"User-Agent": "Mozilla/5.0"})
        except requests.exceptions.RequestException as e:
            raise self.RequestException(e)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup
        # TODO: save results in a variable and return it or save theme in database

    def get_last_job_link(self):
        link = Job.objects.get_last_job_link(self.site_id)
        return link

    class RequestException(Exception):
        pass

    def scroll_down(self):
        start = time.time()
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            end = time.time()
            if round(end - start) > 5:
                break

# class Jobs:
#     def __init__(self, url=init_url, item_count=25, page_item_number=20):
#         self.url = url
#         self.item_count = item_count
#         self.page_count = math.ceil(item_count / page_item_number)
#         self.last_page_item = item_count % page_item_number
#         self.rang = range(self.page_count, 0, -1)
#         self.job_results = []
#         self.image_regex = r'https?:\/\/storage.jobinjacdn.com/other/files/uploads/images/[\s\S]*'
#
#     def get_page_result(self):
#         page_results = []
#         for page in self.rang:
#             try:
#                 response = requests.get(
#                     self.url + f"&page={page}" if page != 1 else self.url,
#                     headers={"User-Agent": "Mozilla/5.0"}
#                 )
#             except requests.exceptions.RequestException as e:  # This is the correct syntax
#                 raise RequestException(e)
#             soup = BeautifulSoup(response.content, "html.parser")
#             result = (
#                 soup.findAll("div", attrs={"class": "o-listView__itemInfo"})[:self.last_page_item]
#                 if len(self.rang) == page
#                 else soup.findAll("div", attrs={"class": "o-listView__itemInfo"})
#             )
#             page_results.append(result)
#         return page_results
#
#     def get_job_results(self, page_results):
#         for page in page_results:
#             for item in page[::-1]:
#                 link_element = item.find("a", class_="c-jobListView__titleLink")
#                 link = link_element.get("href")
#                 title = link_element.text.strip()
#                 time = item.find("span", class_="c-jobListView__passedDays")
#                 image = item.find("img", class_="o-listView__itemIndicatorImage")
#                 match = re.search(self.image_regex, image["src"])
#                 image_link = None
#                 if match:
#                     image_link = match.group()
#                 date = self.generate_item_date(time)
#                 self.job_results.append({
#                     "title": title,
#                     "published_at": date,
#                     "image": image_link,
#                     "link": link
#                 })
#         # return self.job_results
#
#     def save_jobs_in_db(self):
#         for idx, item in enumerate(self.job_results[::-1]):
#             if self.get_last_job_title() == item["link"]:
#                 return "almost_success"
#             if idx == 0: item.update({"is_last": True})
#             Job.objects.create(**item)
#         return "success"
#
#     def get_job_detail_data(self):
#         for job in self.job_results:
#             try:
#                 response = requests.get(job.get("link"), headers={"User-Agent": "Mozilla/5.0"})
#             except requests.exceptions.RequestException as e:
#                 raise RequestException(e)
#             soup = BeautifulSoup(response.content, "html.parser")
#             result = soup.findAll("div", attrs={"class": "o-box__text"})
#             print(result[0].text)
#             # TODO: save results in a variable and return it or save theme in database
#
#     @staticmethod
#     def get_last_job_title():
#         title = Job.objects.get_last_job_title()
#         return title
#
#     @staticmethod
#     def generate_item_date(time):
#         generated_time = unidecode(
#             time.text.translate({ord(i): None for i in '()'}).replace("پیش", "").replace("روز", "").strip()
#         )
#         time_to_number = 0 if generated_time == "m" else int(generated_time)
#         now_date = datetime.datetime.now()
#         item_date = datetime.timedelta(days=time_to_number)
#         result_date = now_date - item_date
#         return result_date.date()
