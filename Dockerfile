FROM python:latest

WORKDIR /src

COPY  ./requirements.txt  /src

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple


COPY . .

CMD ["uvicorn", "main.py:app" , "--host", "0.0.0.0","--port","8000"] 