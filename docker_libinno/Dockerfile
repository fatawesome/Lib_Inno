FROM frolvlad/alpine-python3
WORKDIR /itp_project
RUN pip install django
RUN apk update && \
    apk add --repository http://dl-cdn.alpinelinux.org/alpine/edge/main --no-cache py3-psycopg2
