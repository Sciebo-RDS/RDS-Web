FROM node:15.8-alpine3.10 AS web
WORKDIR /web
ADD / .
RUN apk add gettext
RUN make l10n-compile
RUN npm install
RUN npm run build

FROM python:3.8-alpine
WORKDIR /app
COPY --from=web /web/dist ./dist
ADD /server.py /websocket.py ./

ENTRYPOINT [ "python", "server.py" ]
