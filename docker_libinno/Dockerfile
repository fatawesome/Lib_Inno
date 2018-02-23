FROM frolvlad/alpine-python3
COPY requirements.txt /libinno/
WORKDIR /libinno
RUN pip install django
RUN pip install djangorestframework
RUN pip install markdown
RUN pip install django-filter
RUN pip install -r /libinno/requirements.txt
RUN apk update && \
    apk add --repository http://dl-cdn.alpinelinux.org/alpine/edge/main --no-cache py3-psycopg2
