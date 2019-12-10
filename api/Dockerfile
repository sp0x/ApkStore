#FROM python:3.6-alpine
FROM python:3.7-alpine

RUN mkdir -p /app
WORKDIR /app

RUN apk add --no-cache --virtual .build-deps make gcc musl-dev build-base libxml2-dev libxslt-dev
ADD requirements.txt .
RUN pip install --no-cache -r requirements.txt

#RUN apk add git; \
#    git clone https://github.com/appknox/pyaxmlparser.git && \
#    cd pyaxmlparser; \
#    python setup.py install; \
#    cd ..; rm -rf pyaxmlparser

ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ADD . .


ENTRYPOINT ["/entrypoint.sh"]
