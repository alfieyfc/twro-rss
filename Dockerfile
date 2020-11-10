FROM python:latest

RUN pip install --upgrade pip \
    && pip install requests line-bot-sdk

ENV TZ=Asia/Taipei

COPY ./main.py /app/main.py

CMD python /app/main.py