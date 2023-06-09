# Generated by Django 4.2 on 2023-05-28 03:07

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_module', '0007_site_alter_job_options_alter_job_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobSeeker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='', verbose_name='images')),
                ('image', models.TextField(blank=True, null=True, validators=[django.core.validators.URLValidator()], verbose_name='آدرس تصویر')),
                ('link', models.TextField(blank=True, null=True, validators=[django.core.validators.URLValidator()], verbose_name='لینک صفحه آگهی')),
                ('is_last', models.BooleanField(default=False, verbose_name='آخرین آیتم')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_module.site')),
            ],
            options={
                'verbose_name': 'کارجو',
                'verbose_name_plural': 'کارجو ها',
                'ordering': ['-created_at'],
            },
        ),
    ]
