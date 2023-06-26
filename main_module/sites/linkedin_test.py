from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import DesiredCapabilities
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
    def __init__(self, url=init_url, item_count=20, page_item_number=20):
        super().__init__(url, item_count, page_item_number)
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Firefox(options=options, executable_path="/home/ubuntu/web_driver/geckodriver")
        # self.driver = webdriver.Remote("http://selenium:4444/wd/hub", DesiredCapabilities.FIREFOX, options=options)
        self.site_id = Site.objects.get(title="linkedin").id

    def autologin(self, username="amirdks84@gmail.com", password="61683550",
                  url="https://www.linkedin.com/uas/login"):
        try:
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
        except WebDriverException as e:
            raise self.RequestException("check your internet connection")

    def get_page_result(self):
        self.autologin()
        time.sleep(5)
        try:
            self.driver.get(self.url)
        except WebDriverException as e:
            raise self.RequestException("check your internet connection")
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

    def chatgpt(self):
        self.autologin()
        url = "https://www.linkedin.com/jobs/search/?location=Worldwide&sortBy=DD"
        self.driver.get(url)
        time.sleep(5)
        no_of_jobs = int(
            self.driver.find_element_by_css_selector('h1 > span').get_attribute('innerText').replace('+', '').replace(
                ",", '')
        )
        i = 2
        while i <= int(25 / 25) + 1:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            i = i + 1
            try:
                self.driver.find_element_by_xpath(' / html / body / main / div / section / button').click()
                time.sleep(5)
            except:
                pass
                time.sleep(5)
        # print(self.driver.page_source)
        # return "okab"
        jobs_lists = self.driver.find_element_by_class_name('jobs-search__results-list')
        jobs = jobs_lists.find_elements_by_tag_name('li')[:25]  # return a list
        for job in jobs:
            job_title0 = job.find_element_by_css_selector('h3').get_attribute('innerText')
            company_name0 = job.find_element_by_css_selector('h4').get_attribute('innerText')
            location0 = job.find_element_by_css_selector('[class="job-search-card__location"]').get_attribute(
                'innerText')
            date0 = job.find_element_by_css_selector('div > div > time').get_attribute('datetime')
            job_link0 = job.find_element_by_css_selector('a').get_attribute('href')
            image = job.find_element_by_css_selector('img').get_attribute('src')
            job_res = {
                "title": job_title0,
                "published_at": date0,
                "image": image,
                "link": job_link0,
                "site_id": self.site_id
            }
            self.job_results.append(job_res)

        # print(
        #     {"job_id": job_id, "job_title": job_title, "company_name": company_name, "location": location, "date": date,
        #      "job_link": job_link, })
        self.driver.close()
        return "success"

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
