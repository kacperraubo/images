# base image
FROM python:3.8-slim-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# set entrypoint.sh as the entrypoint script
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
