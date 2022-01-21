# Code evnvironment, lightweight python3.10 alpine
FROM python:3.9.7

#File Author/Maintainer
MAINTAINER Mathemartins


ENV PYTHONUNBUFFERED 1

RUN mkdir -p /var/projects/socialiga

# specify the working dir inside the container
WORKDIR /var/projects/socialiga

ADD requirements.txt /var/projects/socialiga

#install requirements from txt file
RUN pip install --no-cache-dir -r requirements.txt

# add current dir's content to container's WORKDIR root i.e. all the contents of the web app
ADD . /var/projects/socialiga

#Expose port 8000 on docker virtual network
EXPOSE 8000