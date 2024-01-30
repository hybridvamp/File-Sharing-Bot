FROM python:3.11-slim-bookworm
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache -r requirements.txt

COPY . .

CMD python3 bot.py

# FROM python:3

# WORKDIR /app

# COPY . /app

# RUN pip3 install -U -r requirements.txt

# CMD python3 bot.py
