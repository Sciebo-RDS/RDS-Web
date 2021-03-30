# rds-web

The application to get RDS into the new OC Web, the old OC Classic and a standalone interface.

## Dependencies

This application needs pipenv, npm (best option through nvm), yarn, gettext, make, [go](https://golang.org/dl/), tmux, git and [docker](https://docs.docker.com/get-docker/).

```
pip install pipenv
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.2/install.sh | bash
nvm install --lts
npm install yarn
```

If you use ubuntu, you can use for some dependencies `make install` in root.

## Project setup

### Client setup
```bash
cd client
yarn install
```

### Server setup
```bash
cd server
pipenv install
```

### hot-reloads for development

#### standalone
```
make standalone
```

#### classic
```
make classic
```

#### web
```
make web
```

Beware: For testing or using, you need access to a [working RDS instance](https://www.research-data-services.org/doc/getting-started/k8s/).

### Run tests

Runs the tests for vue and python after each other. If the first one fails, then the second one will not executed.

```
make test
```

### Compiles and minifies for production in standalone
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
