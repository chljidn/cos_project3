FROM python:3.6.7

ENV PYTHONUNBUFFERED 1
ENV home/ubuntu/anaconda3/envs/cos_project3

RUN apt-get -y update
RUN apt-get -y install vim

RUN mkdir /srv/docker-server
ADD . /srv/docker-server

WORKDIR /srv/docker-server

RUN pip install --upgrade pip
run pip install -r requirements.txt

EXPOSE 8000
EXPOSE 6379
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000","127.0.0.1:6379"]

