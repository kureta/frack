FROM capsulecode/singlefile:v1.0.33

USER root
RUN apk add --no-cache py3-pip=22.3.1-r1

USER chrome
RUN pip3 install --no-cache-dir --user yt-dlp==2023.12.30
ENV PATH="${PATH}:/home/chrome/.local/bin"
ENV PATH="${PATH}:/usr/src/app/node_modules/single-file-cli"

RUN mkdir /usr/src/app/data
WORKDIR /usr/src/app

ENTRYPOINT []
