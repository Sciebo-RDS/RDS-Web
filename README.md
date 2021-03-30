# rds-web

The application to get RDS into the new OC Web, the old OC Classic and a standalone interface.

## Dependencies

This application needs different software for different integrations.

### All
- make
- tmux
- git

### Server
- pipenv
- [docker](https://docs.docker.com/get-docker/).

### Webfrontend
- npm lts (best option through [nvm](https://github.com/nvm-sh/nvm#install--update-script) `nvm install --lts`)
- yarn `npm install yarn`
- gettext

All nodejs dependencies can be installed through `yarn install` in `/client`.

### Classic
- [php composer](https://getcomposer.org/download/)
- [docker](https://docs.docker.com/get-docker/).

Composer package file can be found in `/client/packages/classic/php/composer.json`.
Docker-compose file can be found in `/client/dev/docker-compose.yml`.

### OC Web
- [go](https://golang.org/dl/)


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
