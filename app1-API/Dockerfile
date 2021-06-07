# syntax=docker/dockerfile:1

FROM python:3.8

RUN apt-get update && apt-get -y install cron vim

WORKDIR /app

COPY requirements.txt requirements.txt

COPY .bash_profile .bash_profile

COPY app.py app.py

COPY crontab /etc/cron.d/crontab

RUN chmod 777 /etc/cron.d/crontab


RUN pip3 install -r requirements.txt

RUN /usr/bin/crontab /etc/cron.d/crontab

COPY . .

# ENTRYPOINT ["cron", "-f"]

CMD ["python3", "/app/app.py"]

#CMD ["cron", "-m", "/tmp/cronlog.txt"]




