# Generated by Django 4.2 on 2023-06-27 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_module', '0010_scrapingsetting'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='icon_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/icons'),
        ),
    ]
