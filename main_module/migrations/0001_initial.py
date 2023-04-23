# Generated by Django 4.2 on 2023-04-21 16:49

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='عنوان آگهی')),
                ('published_at', models.DateField(verbose_name='زمان انتشار آگهی')),
            ],
            options={
                'verbose_name': 'شغل',
                'verbose_name_plural': 'شغل ها',
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]
