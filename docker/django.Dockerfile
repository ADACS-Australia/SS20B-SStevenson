FROM python:3.8 as build
ENV PYTHONUNBUFFERED 0
ENV VIRTUAL_ENV /opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR ${VIRTUAL_ENV}
RUN apt-get update && apt-get install -y python-wheel python-dev python3-dev default-libmysqlclient-dev 
RUN apt-get install -y libmariadb3 libmariadb-dev build-essential libffi-dev
COPY src/requirements.txt requirements.txt
RUN pip install -r requirements.txt

FROM python:3.8-slim
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV /opt/venv
RUN apt-get update && apt-get install -y python-dev python3-dev default-libmysqlclient-dev 
RUN apt-get update && apt-get install -y wget

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

COPY --from=build ${VIRTUAL_ENV} ${VIRTUAL_ENV}

RUN mkdir /files
RUN mkdir /code

WORKDIR /code
COPY src /code/

ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

EXPOSE 8000

