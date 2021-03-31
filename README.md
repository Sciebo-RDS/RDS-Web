# rds-web

The application to get RDS into the new OC Web, the old OC Classic and a standalone interface.

## Dependencies

This application needs different software for different integrations.

For all, you need:
- make
- tmux
- git

For the server backend (owncloud classic and rds), you need:
- pipenv
- [docker](https://docs.docker.com/get-docker/).

*Docker-compose file can be found in `/client/dev/docker-compose.yml`*

For webfrontend, you need:
- npm lts (best option through [nvm](https://github.com/nvm-sh/nvm#install--update-script) `nvm install --lts`)
- yarn `npm install yarn`
- gettext

All nodejs dependencies can be installed through `yarn install` in folder `/client`.

If you want to change the classic integration, you need the following software aswell:
- [php composer](https://getcomposer.org/download/)

Composer package file can be found in `/client/packages/classic/php/composer.json`.

## Notice

In `/client/dev/ocis` you can find the sourcecode for ocis. Currently, we do not develope our software for this backend, so we only use the owncloud classic backend. But for further development, this sourcecode will be needed. For this software, we will need the following software:
- [go](https://golang.org/dl/)

Run `git submodule update --init --recursive` to pull ocis and web servercode.

## Steps for development environment

If you use ubuntu, you can use for some dependencies `make install` in root.
Otherwise, please follow the steps.

### Configuration

We use the dotenv mechanic to provide a simple interface for configuration, which is compatible with the environment workflow of docker and kubernetes. So please configure the .env file to your needs.

```bash
cp .env.example .env
vi .env
```

The fields are:
| name                           | description                                                                                                    |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| `VUE_APP_REDIRECTION_URL`      | Url for redirection for oauth2 workflow.                                                                       |
| `VUE_APP_SKIP_REDIRECTION`     | If you want to use an integration, you don't want to be redirected through webserver or vue app automatically. |
| `OWNCLOUD_OAUTH_CLIENT_SECRET` | Secret token for oauth2.                                                                                       |
| `VERIFY_SSL`                   | For production-use set this to `True`, otherwise no ssl verification.                                          |
| `DEV_FLASK_DEBUG`              | If this is true, the `DEV_FLASK_USERID` name will be used for test purpose.                                    |
| `FLASK_ORIGINS`                | This hosts will be enabled in CORS.                                                                            |

The `VUE_APP_REDIRECTION_URL` and `OWNCLOUD_OAUTH_CLIENT_SECRET` fields can only be set up correctly, when you start up the corresponding oauth backend before. So you have to start the backends and configure the `.env` file properly. After this, you can stop everything and can use the receipts in the corresponding sections for use.


For easier access, you should start only the owncloud backend with the following commands and enable the `oauth2` and `rds` app and add a new oauth2 path in the settings, which is described [here](https://doc.owncloud.com/server/admin_manual/installation/apps_management_installation.html), [here](https://doc.owncloud.com/server/admin_manual/configuration/server/security/oauth2.html#installation) and [here](https://www.research-data-services.org/doc/impl/plugins/owncloud/).

```bash
docker-compose -f client/dev/docker-compose.yml up -d
```

Now open the url `http://localhost:8000` in your favourite browser and enable and setup all needed apps. After this, you have all informations to configure the `.env` correctly. Now, you can continue with the setup.

Remind: If you delete all docker-resources (e.g. with `docker system prune --volumes`), you have to do all steps before again to get valid values for `.env` file.

### Client setup

Install all nodejs dependencies.
```bash
yarn --cwd client install
yarn --cwd client/dev/web install
```

If you use the owncloud classic backend, you will need to install the php dependencies, too.
```bash
composer install --working-dir=client/packages/classic/php 
```

### Server setup

Install the python dependencies.
```bash
cd server
pipenv install
```

### Start the development environments

For easier access, we provide a makefile in root folder.

Beware: For testing or using, you need access to a [working RDS instance](https://www.research-data-services.org/doc/getting-started/k8s/).

If you want to start the environment for standalone, use the `standalone` receipt.
```bash
make standalone
```

If you want to start the environment for owncloud classic with classic ui, use the `classic` receipt.
```bash
make classic
```

If you want to start the environment for ownclouds new ui OC Web with classic backend, use the `web` receipt.
```bash
make web
```

If you want to start the environment for owncloud new ui OC Web with ocis backend, we currently have no receipt.

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
