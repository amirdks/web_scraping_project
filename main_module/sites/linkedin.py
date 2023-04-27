import requests
from bs4 import BeautifulSoup

from main_module.sites.Jobs import Jobs

init_url = "https://www.linkedin.com/jobs/search/?&location=Worldwide&sortBy=DD"


class Linkedin(Jobs):
    def __init__(self, url=init_url, item_count=30, page_item_number=24):
        self.page_item_number = page_item_number
        super().__init__(url, item_count, page_item_number)

    def get_page_result(self):
        page_results = []
        for page in self.rang:
            try:
                response = requests.get(
                    self.url + f"&start={page * self.page_item_number}" if page != 1 else self.url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0",
                        "Host": "www.linkedin.com",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "Accept-Language": "en-US,en;q=0.5",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Connection": "keep-alive",
                        "Upgrade-Insecure-Requests": "1"
                    }
                )
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                raise self.RequestException(e)
            soup = BeautifulSoup(response.content, "html.parser")
            result = (
                soup.findAll("div", attrs={
                    "class": "base-card"})
                [:self.last_page_item]
                if len(self.rang) == page
                else soup.findAll("div", class_="base-card")
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
