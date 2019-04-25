FROM python:3.7-alpine

RUN mkdir /app

COPY requirements.txt /app

COPY *.py /usr/bin

ENV HOME /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["request.template.py"]
