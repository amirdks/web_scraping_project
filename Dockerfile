FROM python:3.11-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SUPERUSER_PASSWORD admin
ENV C_FORCE_ROOT true
RUN apt-get update
RUN apt update
RUN apt-get install -y build-essential libpq-dev
RUN rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt
#CMD while ! python3 manage.py sqlflush > /dev/null 2>&1 ; do sleep 1; done && \
#    python3 manage.py makemigrations --noinput && \
#    python3 manage.py migrate --noinput && \
#    python3 manage.py collectstatic --noinput --clear && \
#    python3 manage.py createsuperuser --user admin --username admin --phone_number 09302483540 --noinput; \
#    gunicorn -b 0.0.0.0:8000 mentoor2.wsgi