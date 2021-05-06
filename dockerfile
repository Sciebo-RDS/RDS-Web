FROM node:14-alpine3.10 AS web
WORKDIR /app
RUN apk add gettext
COPY /client/package.json /client/yarn.lock ./
RUN yarn install
COPY /client .
RUN yarn standalone

FROM python:3.8-alpine
WORKDIR /app
RUN apk add --no-cache nginx gcc musl-dev python3-dev libffi-dev openssl-dev cargo g++
RUN mkdir -p /run/nginx
RUN mkdir -p /var/lib/nginx/tmp
COPY ./server/requirements.txt .
RUN pip install setuptools wheel setuptools-rust
RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=web /app/dist /usr/share/nginx/html
COPY ./server/starter.py .
COPY ./server/src ./src

CMD gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:5000 starter:app --log-level debug --daemon && \
    nginx -g 'daemon off;'
