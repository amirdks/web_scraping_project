
# Web Scraoing Using Python,Django,Celery,Redis
a proejct for data extraction with python and web scraping from divar, jobinja and linkedin with different methods




## Installation

create venv and run project

```bash
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  python manage.py makemigrations
  python manage.py migrate
  python manage.py createsuperuser
  python manage.py runserver
```

**point :** check your redis service 


run celery and celery beat for auto fetching data from sites

```bash
  celery -A core worker -l INFO
  celery -A core.app beat
```

And enjoy using it :)