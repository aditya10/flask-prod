FROM python:3.6

#update
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
        libatlas-base-dev gfortran nginx supervisor
RUN pip install uwsgi

#install requirements
COPY requirements.txt /tmp/requirements.txt
WORKDIR /tmp
RUN pip install -r /tmp/requirements.txt

#create nginx user
RUN useradd --no-create-home nginx

#remove nginx defaults
RUN rm /etc/nginx/sites-enabled/default
RUN rm -r /root/.cache

#copy nginx configs
COPY nginx.conf /etc/nginx/
COPY flask-site-nginx.conf /etc/nginx/conf.d/
COPY uwsgi.ini /etc/uwsgi/
COPY supervisord.conf /etc/

#copy models
#COPY application/models /models/best-model.pt
#COPY application/models /models/export.pkl
#WORKDIR /models
#RUN chmod -R 777 ./

#copy app
ADD ./application /
WORKDIR /application

#start supervisor
CMD ["/usr/bin/supervisord"]