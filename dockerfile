FROM node:15.8-alpine3.10 AS web
WORKDIR /app
RUN apk add gettext
COPY /client/package.json /client/package-lock.json ./
RUN npm install
COPY /client .
RUN npm run build

FROM python:3.8-alpine
WORKDIR /app
RUN apk add --no-cache nginx gcc musl-dev python3-dev libffi-dev openssl-dev cargo g++
RUN mkdir -p /run/nginx
RUN mkdir -p /var/lib/nginx/tmp
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY ./server/requirements.txt .
RUN pip install setuptools wheel setuptools-rust
RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY --from=web /app/dist /usr/share/nginx/html
COPY ./server/starter.py .
COPY ./server/src ./src

CMD gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:5000 starter:app --daemon && \
    nginx -g 'daemon off;'
