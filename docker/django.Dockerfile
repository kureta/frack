FROM python:3.11-alpine

RUN apk upgrade --no-cache --available \
  && apk add --no-cache py3-pip=23.3.1-r0

RUN mkdir -p /usr/src/app \
  && adduser -D django \
  && chown -R django:django /usr/src/app

USER django

ENV PATH="${PATH}:/home/django/.local/bin"

RUN pip3 install --no-cache-dir --user \
  hatch==1.9.3

WORKDIR /usr/src/app

COPY . /usr/src/app/
RUN hatch env create

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

ENTRYPOINT ["hatch", "run", "python", "src/manage.py", "runserver", "0.0.0.0:8000"]
