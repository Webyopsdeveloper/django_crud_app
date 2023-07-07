# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.6
# pull official base image
#FROM python:3.8.3-alpine as builder
# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
#RUN mkdir /rest_api

# Set the working directory to /music_service
WORKDIR .

# Copy the current directory contents into the container at /music_service
#ADD . /rest_api/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

COPY .. .

EXPOSE 8000

CMD ["python", "manage.py", "runserver"]