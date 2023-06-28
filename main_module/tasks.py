from celery import shared_task

from main_module.job_seekers.jobseeker import JobSeekerClass
from main_module.models import ScrapingSetting
from main_module.sites.Jobs import Jobs
from main_module.sites.divar import Divar
from main_module.sites.jobinja import Jobinja
from main_module.sites.jobvision import JobVision
from main_module.sites.linkedin import Linkedin
from main_module.sites.linkedin_test import LinkedinTest
from utils.fetching_data import fetching_data


@shared_task
def fetch_data_from_jobinja():
    return fetching_data("jobinja", Jobinja)


@shared_task
def fetch_data_from_divar():
    return fetching_data("divar", Divar)


@shared_task()
def fetch_data_from_linkedin():
    return fetching_data("linkedin", LinkedinTest)


@shared_task()
def fetch_data_from_jobseeker():
    return fetching_data("jobseeker", JobSeekerClass)


@shared_task()
def fetch_data_from_jobvision():
    return fetching_data("jobvision", JobVision)
