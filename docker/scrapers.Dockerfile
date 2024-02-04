FROM capsulecode/singlefile:v1.0.33

# Install pip
USER root
RUN --mount=type=cache,target=/var/cache/apk \
    apk update && \
    apk add py3-pip=22.3.1-r1

# Install yt-dlp
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install yt-dlp==2023.12.30

RUN mkdir -p /app
WORKDIR /app

COPY requirements-worker.txt /app/requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

RUN chown -R chrome:chrome /app
USER chrome

ENV PATH="${PATH}:/usr/src/app/node_modules/single-file-cli"

WORKDIR /app

ENTRYPOINT []
