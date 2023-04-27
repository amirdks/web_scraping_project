from celery import shared_task

from main_module.sites.Jobs import Jobs
from main_module.sites.divar import Divar
from main_module.sites.jobinja import Jobinja
from main_module.sites.linkedin import Linkedin
from main_module.sites.linkedin_test import LinkedinTest


# @shared_task
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


# @shared_task
def fetch_data_from_divar():
    job = Divar()
    try:
        page_results = job.get_page_result()
    except job.RequestException as e:
        return "failed"
    job.get_job_results(page_results)
    res = job.save_jobs_in_db()
    print(res)
    return res


# @shared_task()
def fetch_data_from_linkedin():
    job = LinkedinTest()
    try:
        page_results = job.get_page_result()
    except job.RequestException as e:
        return "failed"
    job.get_job_results(page_results)
    res = job.save_jobs_in_db()
    return "success"


# @shared_task
def fetch_data_from_site():
    res = "success"
    # job = Jobinja()
    # job = Divar()
    # try:
    #     page_results = job.get_page_result()
    # except job.RequestException as e:
    #     print(e)
    #     return "failed"
    # job.get_job_results(page_results)
    # res = job.save_jobs_in_db()
    # job.get_job_detail_data()
    # divar = Divar()
    # try:
    #     page_results = divar.get_page_result()
    # except divar.RequestException as e:
    #     print(e)
    #     return "failed"
    # divar.get_job_results(page_results)
    # res = divar.save_jobs_in_db()
    # print(f"divat ==> {res}")
    # job = Jobinja()
    # try:
    #     page_results = job.get_page_result()
    # except job.RequestException as e:
    #     print(e)
    #     return "failed"
    # job.get_job_results(page_results)
    # res = job.save_jobs_in_db()
    # print(f"jobinja ==> {res}")
    # linkedin = LinkedinTest()
    # job_res = linkedin.new_test()
    # print(job_res)
    fetch_data_from_linkedin()
    return res
