# rds-web

The application to get RDS into the new OC Web interface.

## Dependencies

This application needs pipenv and npm (best option through nvm).

```
pip install pipenv
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.2/install.sh | bash
nvm install node
```

## Project setup
```
npm install
pipenv install
```

### hot-reloads for development
```
npm run serve
pipenv run python websocket.py
```

If you have installed `tmux` and `make`, you can use the following command to create the server and client hot reload for development.
```
make test
```
After that, your server will be reachable under `localhost:8080` and the frontend under `localhost:8085`.

### Compiles and minifies for production
We use docker to create containers. This will build a single server, which serves the frontend under port 8080.
This can be build with the following command, which will be stored in the local container storage under the name "rds-web".

```
docker build -t rds-web
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
