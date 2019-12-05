#FROM python:3.6-alpine
FROM python:3.7-alpine

RUN mkdir -p /app
WORKDIR /app

ADD requirements.txt .
RUN pip install --no-cache -r requirements.txt
RUN apk add git-core; \
    git clone https://github.com/appknox/pyaxmlparser.git; \
    cd pyaxmlparser; \
    python setup.py; \
    cd ..; rm -rf pyaxmlparser

ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ADD . .


ENTRYPOINT ["/entrypoint.sh"]
