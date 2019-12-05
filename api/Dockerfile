#FROM python:3.6-alpine
FROM python:3.7-stretch

RUN mkdir -p /app
WORKDIR /app

ADD requirements.txt .
RUN pip install --no-cache -r requirements.txt
ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ADD . .


ENTRYPOINT ["/entrypoint.sh"]
