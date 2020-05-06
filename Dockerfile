FROM python:3.7-slim-buster

ENV PYTHONUNBUFFERED 1

COPY src /src
COPY requirements.txt /
COPY start /

WORKDIR /src

RUN chmod +x /start

RUN pip install -r /requirements.txt

# Install utilities
RUN apt-get update --fix-missing && apt-get -y upgrade
RUN apt-get install -y sudo wget gnupg2 unzip

# Install latest chrome dev package.
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable --no-install-recommends


RUN wget https://github.com/Yelp/dumb-init/releases/download/v1.2.2/dumb-init_1.2.2_amd64.deb
RUN dpkg -i dumb-init_1.2.2_amd64.deb
RUN rm dumb-init_1.2.2_amd64.deb

RUN wget -q -O - https://deb.nodesource.com/setup_10.x | bash - \
    && apt-get install -y nodejs

# Download latest Lighthouse from npm.
# cache bust so we always get the latest version of LH when building the image.
ARG CACHEBUST=1
RUN npm i lighthouse -g

# Disable Lighthouse error reporting to prevent prompt.
ENV CI=true

## Add a chrome user so we can execute chrome properly.
RUN groupadd --system chrome && \
    useradd --system --create-home --gid chrome --groups audio,video chrome && \
    mkdir --parents /home/chrome/reports && \
    chown --recursive chrome:chrome /home/chrome

USER chrome

ENTRYPOINT ["/usr/bin/dumb-init", "--"]

EXPOSE 3000
