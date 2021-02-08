FROM node:15.8-alpine3.10 AS web
RUN apk add gettext make
RUN npm install
WORKDIR /web
COPY . .
RUN make l10n-compile
RUN npm run build

FROM python:3.8-alpine
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY --from=web /web/dist ./dist
COPY ./server.py ./websocket.py /dist/

ENTRYPOINT [ "python", "server.py" ]
