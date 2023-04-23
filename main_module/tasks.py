import math

import requests
from bs4 import BeautifulSoup
from celery import shared_task

from main_module.Jobs import Jobs, RequestException
from main_module.models import Job


# # @shared_task
# def fetch_data_from_site():
#     item_count = 25
#     page_count = math.ceil(item_count / 20)
#     last_page_item = item_count % 20
#     url = "https://jobinja.ir/jobs/latest-job-post-%D8%A7%D8%B3%D8%AA%D8%AE%D8%AF%D8%A7%D9%85%DB%8C-%D8%AC%D8%AF%DB%8C%D8%AF?preferred_before=1682092785&sort_by=published_at_desc"
#     results = []
#     rang = range(page_count, 0, -1)
#     last_job_title = Job.objects.get_last_job_title()
#     for page in rang:
#         response = requests.get(
#             url + f"&page={page}" if page != 1 else url,
#             headers={"User-Agent": "PostmanRuntime/7.32.2"}
#         )
#         soup = BeautifulSoup(response.content, "html.parser")
#         result = (
#             soup.findAll("div", attrs={"class": "o-listView__itemInfo"})[:last_page_item]
#             if len(rang) == page
#             else soup.findAll("div", attrs={"class": "o-listView__itemInfo"})
#         )
#         for item in result[::-1]:
#             title = item.find("a", class_="c-jobListView__titleLink").text.strip()
#             time = item.find("span", class_="c-jobListView__passedDays")
#             date = generate_item_date(time)
#             results.append({
#                 "title": title,
#                 "published_at": date
#             })
#     for idx, item in enumerate(results[::-1]):
#         if last_job_title == item["title"]: return "break be mola"
#         if idx == 0: item.update({"is_last": True})
#         Job.objects.create(**item)
#     return "oakbe da"


# @shared_task
def fetch_data_from_site():
    job = Jobs()
    try:
        page_results = job.get_page_result()
    except RequestException as e:
        print(e)
        return "failed"
    job.get_job_results(page_results)
    res = job.save_jobs_in_db()
    # job.get_job_detail_data()
    return res
