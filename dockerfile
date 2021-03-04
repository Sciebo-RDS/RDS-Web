FROM node:15.8-alpine3.10 AS web
WORKDIR /app
RUN apk add gettext make
COPY /client/package.json /client/package-lock.json ./
RUN npm install
COPY /client .
RUN make l10n-compile
RUN npm run build

FROM python:3.8-alpine
WORKDIR /app
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY ./server/requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY --from=web /app/dist /usr/share/nginx/html
COPY ./server ./

CMD gunicorn -b 0.0.0.0:5000 app:app --daemon && \
    nginx -g 'daemon off;'
