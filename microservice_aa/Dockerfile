FROM python:3.11.4-buster

LABEL Sobolev Andrey

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip
WORKDIR /app/
COPY requirements.txt requirements.txt
RUN pip3 install -r ./requirements.txt
COPY . .

CMD uvicorn app:app --host 0.0.0.0 --port 14000