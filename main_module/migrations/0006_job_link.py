# Generated by Django 4.2 on 2023-04-23 15:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_module', '0005_alter_job_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='link',
            field=models.TextField(blank=True, null=True, validators=[django.core.validators.URLValidator()]),
        ),
    ]
