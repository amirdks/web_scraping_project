from celery import shared_task
from main_module.utils import fetch_data_from_jobseeker, fetch_data_from_jobinja, fetch_data_from_divar, \
    fetch_data_from_jobvision, fetch_data_from_irantalent, fetch_data_from_e_estekhdam


# @shared_task
# def fetch_data_from_jobinja():
#     return fetching_data("jobinja", Jobinja)
#
#
# @shared_task
# def fetch_data_from_divar():
#     return fetching_data("divar", Divar)
#
#
# @shared_task()
# def fetch_data_from_linkedin():
#     return fetching_data("linkedin", LinkedinTest)
#
#
# @shared_task()
# def fetch_data_from_jobseeker():
#     return fetching_data("jobseeker", JobSeekerClass)
#
#
# @shared_task()
# def fetch_data_from_jobvision():
#     return fetching_data("jobvision", JobVision)
#
#
# @shared_task()
# def fetch_data_from_irantalent():
#     return fetching_data("irantalent", Irantalent)
#
#
# @shared_task()
# def fetch_data_from_e_estekhdam():
#     return fetching_data("e_estekhdam", EEstekhdam)
@shared_task()
def fetch_full_data():
    try:
        fetch_data_from_jobseeker()
        fetch_data_from_jobinja()
        fetch_data_from_divar()
        fetch_data_from_jobvision()
        fetch_data_from_irantalent()
        fetch_data_from_e_estekhdam()
        return "success"
    except Exception as e:
        return f"failed ==> {e}"
