FROM python:latest

WORKDIR /src

COPY  ./requirements.txt  /src

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY .  /src

CMD [ "pyhton" "main.py"]
