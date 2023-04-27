from django.core.validators import URLValidator
from django.db import models
from django.db.models.expressions import NoneType


# Create your models here.

class Site(models.Model):
    title = models.CharField(max_length=255, unique=True)
    base_url = models.TextField(validators=[URLValidator()], null=True, blank=True)
    last_update = models.DateTimeField()
    created_at = models.DateField(auto_now_add=True)


class JobManager(models.Manager):
    def get_last_job_link(self, site_id):
        if site_id is not None:
            try:
                link = self.filter(is_last=True, site_id=site_id).last().link
            except:
                link = ""
        else:
            try:
                link = self.filter(is_last=True).last().link
            except:
                link = ""
        return link


class Job(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name="عنوان آگهی")
    published_at = models.DateField(verbose_name="زمان انتشار آگهی")
    # image = models.ImageField(upload_to='images/logo', verbose_name='تصویر لوگو', null=True, blank=True)
    image = models.TextField(validators=[URLValidator()], null=True, blank=True, verbose_name="آدرس تصویر")
    link = models.TextField(validators=[URLValidator()], null=True, blank=True, verbose_name="لینک صفحه آگهی")
    is_last = models.BooleanField(default=False, verbose_name="آخرین آیتم")
    objects = JobManager()

    class Meta:
        verbose_name = "شغل"
        verbose_name_plural = "شغل ها"
        ordering = ["-published_at"]

    def __str__(self):
        return self.title
