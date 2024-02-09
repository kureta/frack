FROM python:3.11-alpine

# Install pip
RUN --mount=type=cache,target=/var/cache/apk \
    apk update && \
    apk add py3-pip=23.3.1-r0

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

RUN adduser -D django \
    && chown -R django:django /app
USER django

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

CMD ["python3", "src/manage.py", "runserver", "0.0.0.0:8000"]
