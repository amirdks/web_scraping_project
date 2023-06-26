from celery import shared_task

from main_module.job_seekers.jobseeker import JobSeekerClass
from main_module.models import ScrapingSetting
from main_module.sites.Jobs import Jobs
from main_module.sites.divar import Divar
from main_module.sites.jobinja import Jobinja
from main_module.sites.linkedin import Linkedin
from main_module.sites.linkedin_test import LinkedinTest


# @shared_task
def fetch_data_from_jobinja():
    try:
        jobinja_setting = ScrapingSetting.objects.get(site__title="jobinja")
        item_count = jobinja_setting.number
    except ScrapingSetting.DoesNotExist:
        item_count = 20
    job = Jobinja(item_count=item_count)
    try:
        page_results = job.get_page_result()
    except job.RequestException as e:
        return "failed"
    job.get_job_results(page_results)
    res = job.save_jobs_in_db()
    print(res)
    return res


# @shared_task
def fetch_data_from_divar():
    try:
        jobinja_setting = ScrapingSetting.objects.get(site__title="divar")
        item_count = jobinja_setting.number
    except ScrapingSetting.DoesNotExist:
        item_count = 20
    job = Divar(item_count=item_count)
    try:
        page_results = job.get_page_result()
    except job.RequestException as e:
        return "failed"
    job.get_job_results(page_results)
    res = job.save_jobs_in_db()
    return res


# @shared_task()
def fetch_data_from_linkedin():
    try:
        jobinja_setting = ScrapingSetting.objects.get(site__title="linkedin")
        item_count = jobinja_setting.number
    except ScrapingSetting.DoesNotExist:
        item_count = 20
    job = LinkedinTest(item_count=item_count)
    try:
        page_results = job.get_page_result()
        job.get_job_results(page_results)
        res = job.save_jobs_in_db()
        return "success"
    except job.RequestException as e:
        print("failed")
        print("error =>>", e)
        return "failed returned"


# @shared_task()
def fetch_data_from_jobseeker():
    try:
        jobinja_setting = ScrapingSetting.objects.get(site__title="jobseeker")
        item_count = jobinja_setting.number
    except ScrapingSetting.DoesNotExist:
        item_count = 20
    job = JobSeekerClass(item_count=item_count)
    try:
        page_results = job.get_page_result()
        job.get_job_results(page_results)
        res = job.save_jobs_in_db()
        return "success"
    except job.RequestException as e:
        print("failed")
        print("error =>>", e)
        return "failed returned"

# @shared_task
# def fetch_data_from_site():
#     fetch_data_from_divar()
#     return "res"
