FROM python:3.7-slim-buster

ENV PYTHONUNBUFFERED 1

COPY ./grader /app

RUN apt-get update \
    # dependencies for building Python packages
    && apt-get install -y build-essential \
    # Google chrome
    && apt-get install -y wget xvfb unzip \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update -y \
    && apt-get install -y google-chrome-stable \
    # !!!!! CLEANUP !!!!!
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./docker/start /start
RUN chmod +x /start

WORKDIR /app
