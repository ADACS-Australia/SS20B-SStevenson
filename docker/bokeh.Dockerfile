FROM python:3.7-slim
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

WORKDIR /code

COPY src/plots /code/

RUN pip install --no-cache-dir -r requirements.txt