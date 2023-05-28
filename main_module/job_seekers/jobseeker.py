import datetime

import requests
from bs4 import BeautifulSoup

from main_module.models import JobSeeker, Site
from main_module.sites.Jobs import Jobs

init_url = 'https://daneshmandjobs.com/candidates/'


class JobSeekerClass(Jobs):
    def __init__(self, url=init_url, item_count=10, page_item_number=12):
        super(JobSeekerClass, self).__init__(url, item_count, page_item_number)
        self.image_regex = r'https?:\/\/storage.jobinjacdn.com/other/files/uploads/images/[\s\S]*'
        self.base_url = "https://daneshmandjobs.com"
        self.site_id = Site.objects.get(title="jobseeker").id

    def save_jobs_in_db(self):
        duplicated_job_items = JobSeeker.objects.filter(site_id=self.site_id, link__in=self.links_list).values_list(
            "link")
        duplicated = [link[0] for link in duplicated_job_items]
        res = [x for x in self.job_results if x["link"] not in duplicated]
        for idx, item in enumerate(res[::-1]):
            # if self.get_last_job_link() == item["link"]:
            #     return "almost_success"
            if idx == 0: item.update({"is_last": True})
            JobSeeker.objects.create(**item)
        return "success"

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
                soup.findAll("div", attrs={"class": "candidate-item"})[
                :self.last_page_item]
                if len(self.rang) == page
                else soup.findAll("div", attrs={"class": "candidate-item"})
            )
            page_results.append(result)
        return page_results

    def get_job_results(self, page_results):

        for page in page_results:
            for item in page[::-1]:
                link_element = item.find("a")
                link = link_element.get("href")
                full_name = item.find("h3", class_="candidate-title").find("a").text.strip()
                # time = item.find("span", class_="kt-post-card__bottom-description kt-text-truncate").text.strip()
                # instantaneous = item.find("span", class_="kt-post-card__red-text")
                # if instantaneous:
                #     time = "instantaneous"
                image = item.find("img")
                image_link = None
                if image:
                    image_link = image.get("data-lazy-src")
                date = datetime.datetime.now()
                self.links_list.append(link)
                result = {
                    "full_name": full_name,
                    "image": image_link,
                    "link": link,
                    "site_id": self.site_id
                }
                self.job_results.append(result)
