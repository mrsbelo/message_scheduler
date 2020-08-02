FROM python:3.8.1-slim-buster
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y netcat

RUN pip install --upgrade pip
COPY ./requirements/ /app/requirements/
RUN pip install -r requirements/dev.txt

COPY . /app/
ENTRYPOINT ["/app/entrypoint.sh"]