from django.core.validators import URLValidator
from django.db import models
from django.db.models.expressions import NoneType


# Create your models here.


class JobManager(models.Manager):
    def get_last_job_title(self):
        try:
            title = self.filter(is_last=True).last().link
        except:
            title = ""
        return title


class Job(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان آگهی")
    published_at = models.DateField(verbose_name="زمان انتشار آگهی")
    # image = models.ImageField(upload_to='images/logo', verbose_name='تصویر لوگو', null=True, blank=True)
    image = models.TextField(validators=[URLValidator()], null=True, blank=True)
    link = models.TextField(validators=[URLValidator()], null=True, blank=True)
    is_last = models.BooleanField(default=False)
    objects = JobManager()

    class Meta:
        verbose_name = "شغل"
        verbose_name_plural = "شغل ها"

    def __str__(self):
        return self.title
