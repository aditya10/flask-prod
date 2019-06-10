FROM python:3.6

#update
RUN apt-get update

#install requirements
COPY requirements.txt /tmp/requirements.txt
WORKDIR /tmp
RUN pip install -r /tmp/requirements.txt
RUN pip install flask gunicorn

#copy app
ADD . /app
WORKDIR /app

#run again, should not download
RUN pip install -r /tmp/requirements.txt

EXPOSE 8000
CMD ["gunicorn", "-w", "5", "-b", "0.0.0.0:8000", "app"]