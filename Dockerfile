FROM python:3.11.12-slim-bullseye

LABEL maintainer="ganguly.aritra@outlook.com"

RUN pip3 install pip --upgrade

# Install Git and other applicable packages.
RUN apt-get update && apt-get install git chromium wget unzip gcc python-dev curl gnupg -y

# Installing `xvfb` is required for headless Chrome; it provides a virtual screen.
RUN apt-get update && apt-get install -y python3-tk python3-dev xvfb && apt upgrade -y
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

# Set the Chrome repo.
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# Install Chrome.
RUN apt-get update && apt-get -y install google-chrome-stable

COPY . .

ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99

RUN pip install .

CMD Xvfb :99 -screen 0 1920x1080x24 & tail -f /dev/null