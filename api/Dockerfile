FROM python:3.6

#update
RUN apt-get update

#install requirements
COPY requirements.txt /tmp/requirements.txt
WORKDIR /tmp
RUN pip install -r /tmp/requirements.txt
RUN pip install flask gunicorn

#copy app
COPY . /app
WORKDIR /app