# Generated by Django 4.2 on 2023-06-25 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_module', '0008_jobseeker'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobseeker',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
