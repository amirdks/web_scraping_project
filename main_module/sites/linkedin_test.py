from selenium import webdriver
from selenium.webdriver.common import by
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import re as re
import time
import pandas as pd

from main_module.models import Site
from main_module.sites.Jobs import Jobs

init_url = "https://www.linkedin.com/jobs/search/?currentJobId=3550746733&location=Worldwide&sortBy=DD"


class LinkedinTest(Jobs):
    def __init__(self, url=init_url):
        super().__init__(url, 25, 20)
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Firefox(options=options)
        self.site_id = Site.objects.get(title="linkedin").id

    def autologin(self, username="amirdks84@gmail.com", password="61683550",
                  url="https://www.linkedin.com/uas/login"):
        self.driver.get(url)
        password_input = self.driver.find_element_by_xpath("//input[@type='password']")
        password_input.send_keys(password)
        username_input = password_input.find_element_by_xpath(
            ".//preceding::input[not(@type='hidden')]")
        username_input.send_keys(username)
        form_element = password_input.find_element_by_xpath(".//ancestor::form")
        submit_button = form_element.find_element_by_xpath(
            ".//*[@type='submit']").click()
        return self.driver

    def get_page_result(self):
        self.autologin()
        time.sleep(5)
        self.driver.get(self.url)
        time.sleep(5)
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
        company_page = self.driver.page_source
        linkedin_soup = bs(company_page.encode("utf-8"), "html.parser")
        linkedin_soup.prettify()
        main_ul = linkedin_soup.find("ul", class_="jobs-search__results-list")
        jobs_container = main_ul.findChildren("li", recursive=False)
        return jobs_container

    # def chatgpt(self):
    #     url = "https://www.linkedin.com/jobs/search/?geoId=92000000&keywords=&location=Worldwide&sortBy=DD"
    #     driver = webdriver.Firefox()
    #     driver.get(url)
    #     time.sleep(5)
    #     jobs = []
    #     soup = bs(driver.page_source, "html.parser")
    #     for element in soup.find_all("li", class_="result-card"):
    #         job = {}
    #         job['title'] = element.find("h3", class_="result-card__title").text.strip()
    #         job['link'] = element.find("a", href=True)['href']
    #         job['image'] = element.find("img", class_="result-card__image")['src']
    #         job['date'] = element.find("time", class_="result-card__datetime")['datetime']
    #         jobs.append(job)
    #     print(jobs)
    #     for job in jobs:
    #         print(job['title'], job['link'], job['image'], job['date'])
    #     driver.close()

    def get_job_results(self, page_results):
        for job in page_results[::-1]:
            title = job.find("span", class_="sr-only")
            link = job.find("a", class_="base-card__full-link")
            image = job.find("img")
            date = job.find("time")
            if title and link and image and date:
                title = title.text.strip()
                link = link.get("href")
                image = image.get("src")
                date = date.get("datetime")
                self.links_list.append(link)
                job_res = {
                    "title": title,
                    "published_at": date,
                    "image": image,
                    "link": link,
                    "site_id": self.site_id
                }
                self.job_results.append(job_res)
        # containers = linkedin_soup.findAll("div", {"class": "occludable-update ember-view"})
