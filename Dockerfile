FROM python:3.12

WORKDIR /src

COPY  ./requirements.txt  /src

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple


COPY . .

ENV PYTHONPATH /src
