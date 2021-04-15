FROM teamcompas/compas:02.18.09

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN mkdir /code
WORKDIR /code

RUN apt-get update && apt-get install -y python-wheel python3-venv
ENV VIRTUAL_ENV /opt/venv
RUN python3 -m venv $VIRTUAL_ENV
WORKDIR ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"
COPY src/requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /code
COPY src /code/
