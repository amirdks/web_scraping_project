from celery import shared_task

from main_module.job_seekers.jobseeker import JobSeekerClass
from main_module.sites.Jobs import Jobs
from main_module.sites.divar import Divar
from main_module.sites.jobinja import Jobinja
from main_module.sites.linkedin import Linkedin
from main_module.sites.linkedin_test import LinkedinTest


@shared_task
def fetch_data_from_jobinja():
    job = Jobinja()
    try:
        page_results = job.get_page_result()
    except job.RequestException as e:
        return "failed"
    job.get_job_results(page_results)
    res = job.save_jobs_in_db()
    print(res)
    return res


@shared_task
def fetch_data_from_divar():
    job = Divar()
    try:
        page_results = job.get_page_result()
    except job.RequestException as e:
        return "failed"
    job.get_job_results(page_results)
    res = job.save_jobs_in_db()
    return res


@shared_task()
def fetch_data_from_linkedin():
    job = LinkedinTest()
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
    job = JobSeekerClass()
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
