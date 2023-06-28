from main_module.models import ScrapingSetting


def fetching_data(site_name, site_class):
    try:
        jobinja_setting = ScrapingSetting.objects.get(site__title=site_name)
        item_count = jobinja_setting.number
    except ScrapingSetting.DoesNotExist:
        item_count = 20
    job = site_class(item_count=item_count)
    try:
        page_results = job.get_page_result()
    except job.RequestException as e:
        return "failed"
    job.get_job_results(page_results)
    res = job.save_jobs_in_db()
    return "res"
