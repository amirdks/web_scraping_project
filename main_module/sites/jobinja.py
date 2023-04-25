import datetime
import re

import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

from main_module.sites.Jobs import Jobs

init_url = "https://jobinja.ir/jobs/latest-job-post-%D8%A7%D8%B3%D8%AA%D8%AE%D8%AF%D8%A7%D9%85%DB%8C-%D8%AC%D8%AF%DB%8C%D8%AF?preferred_before=1682092785&sort_by=published_at_desc"


class Jobinja(Jobs):
    def __init__(self, url=init_url, item_count=25, page_item_number=20):
        super(Jobinja, self).__init__(url, item_count, page_item_number)
        self.image_regex = r'https?:\/\/storage.jobinjacdn.com/other/files/uploads/images/[\s\S]*'

    def get_page_result(self):
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
            result = (
                soup.findAll("div", attrs={"class": "o-listView__itemInfo"})[:self.last_page_item]
                if len(self.rang) == page
                else soup.findAll("div", attrs={"class": "o-listView__itemInfo"})
            )
            page_results.append(result)
        return page_results

    def get_job_results(self, page_results):
        for page in page_results:
            for item in page[::-1]:
                link_element = item.find("a", class_="c-jobListView__titleLink")
                link = link_element.get("href")
                title = link_element.text.strip()
                time = item.find("span", class_="c-jobListView__passedDays")
                image = item.find("img", class_="o-listView__itemIndicatorImage")
                match = re.search(self.image_regex, image["src"])
                image_link = None
                if match:
                    image_link = match.group()
                date = self.generate_item_date(time)
                self.job_results.append({
                    "title": title,
                    "published_at": date,
                    "image": image_link,
                    "link": link
                })

    @staticmethod
    def generate_item_date(time):
        generated_time = unidecode(
            time.text.translate({ord(i): None for i in '()'}).replace("پیش", "").replace("روز", "").strip()
        )
        time_to_number = 0 if generated_time == "m" else int(generated_time)
        now_date = datetime.datetime.now()
        item_date = datetime.timedelta(days=time_to_number)
        result_date = now_date - item_date
        return result_date.date()
