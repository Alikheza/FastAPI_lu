FROM python:3.12

WORKDIR /src

COPY  ./requirements.txt  /src

RUN pip install -r requirements.txt 


COPY . .

ENV PYTHONPATH /src
