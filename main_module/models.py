from django.db import models


# Create your models here.


class JobManager(models.Manager):
    def get_last_job_title(self):
        return self.filter(is_last=True).last().title


class Job(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان آگهی")
    published_at = models.DateField(verbose_name="زمان انتشار آگهی")
    is_last = models.BooleanField(default=False)
    objects = JobManager()

    class Meta:
        verbose_name = "شغل"
        verbose_name_plural = "شغل ها"

    def __str__(self):
        return self.title
