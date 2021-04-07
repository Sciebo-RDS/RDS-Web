# rds-web

The application to get RDS into the new OC Web, the old OC Classic and a standalone interface.

*This application currently only supports the classic backend, which is written in php. Not the ocis backend in golang!*

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

All nodejs dependencies can be installed through `yarn --cwd client install`.

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

### Notices

First, you should think about, what you want to develope. You have the choice of:
- standalone
- owncloud classic
- owncloud Web

`standalone` means, you will be redirected to an oauth server, which handles the login and redirects back, so the user only sees the RDS App in whole. The application does not have any access to informations about the user except the oauth2 access token. This problem will be handled through the rds backend server.

`owncloud classic` means, that the old frontend of owncloud will be used for integration. This is the easierst form of integration, because the standalone app can be loaded and initialized in the same context as the user runs the frontend. Here we will use a jwt for authentication, which will be evaluated on the rds server side.

`owncloud web` is the new standard of owncloud, which implements all extension in vue. This comes with a lot of new problems, so we handle this with an iframe. The communication between the 2 separate windows will be through the event bus of the browser. Here we will use a jwt for authentication, too.

If you have make your choice (you can also choose all three, but then you have to make all steps for e.g. you have to generate 2 clients in your oauth server).

#### Ports

In the following sections, you read a lot about ports. Here you have an overview, which port comes from which service.

| Port | Description                                                                            |
| ---- | -------------------------------------------------------------------------------------- |
| 8000 | Owncloud classic                                                                       |
| 8080 | Python Backend Server, which manages login for websocket and proxy for vue dev server. |
| 8082 | OC Web extension vue dev server, which manages the integration of RDS into OC Web.     |
| 8085 | Vue dev Server for RDS Standalone App                                                  |
| 8100 | Vue dev Server for Describo Standalone App                                             |
| 9100 | new owncloud web vue dev server                                                        |
| 9200 | ocis frontend, which proxies requests to port 9100 (currently not used)                |


### Configuration

We use the dotenv mechanic to provide a simple interface for configuration, which is compatible with the environment workflow of docker and kubernetes. So please configure the .env file to your needs.

```bash
cp .env.example .env
vi .env
```

| fieldname                    | description                                                                                                               | default                                                                                                              |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| OWNCLOUD_URL                 | The url to your owncloud instance.                                                                                        | http://localhost:8000                                                                                                |
| OWNCLOUD_OAUTH_CLIENT_SECRET | The client secret for your oauth provider.                                                                                | XYZ                                                                                                                  |
| EMBED_MODE                   | Set this to True, if you want to use the app in embed mode. False means standalone mode.                                  | True                                                                                                                 |
| FLASK_ORIGINS                | Set here all origins from requests can come. Otherwise it will be rejected through CORS.                                  | ["http://localhost:8080", "http://localhost:8085", "http://localhost:8000", "http://localhost:9100"]                 |
| VUE_APP_REDIRECTION_URL      | Set this URL for redirection in vue app, client-side. Deprecated                                                          | http://localhost:8000/apps/oauth2/authorize?response_type=token&client_id=`<ABC>`&redirect_uri=http://localhost:8080 |
| REDIRECTION_URL              | Set this URL for redirection on serverside through http statuscode 302.                                                   | http://localhost:8000/apps/oauth2/authorize?response_type=token&client_id=`<ABC>`&redirect_uri=http://localhost:8080 |
| VUE_APP_SKIP_REDIRECTION     | Set this to True, if you want to skip the redirection, client-side based. Deprecated                                      | `True`                                                                                                               |
| VUE_APP_DESCRIBO_URL         | Set this URL for your describo instance.                                                                                  | http://localhost:8100                                                                                                |
| VUE_APP_FRONTENDHOST         | Set this URL to your frontend host.                                                                                       | http://localhost:8080                                                                                                |
| VUE_APP_SOCKETIO_HOST        | Set this URL to your socketio host. In this implementation, it is the same as frontendhost.                               | http://localhost:8080                                                                                                |
| DEV_WEBPACK_DEV_SERVER_HOST  | Set this URL to your vue app host, so the frontend host can proxy requests.                                               | "http://localhost:8085"                                                                                              |
| VERIFY_SSL                   | Set this to `True`, if you want to verify ssl certs. `False` if you do not want that.                                     | `False`                                                                                                              |
| DEV_FLASK_DEBUG              | Set this to `True`, if you want more debug informations in console.                                                       | `True`                                                                                                               |
| DEV_USE_PROXY                | Set this to `True`, if you want to use the server as a proxy for vue app. *Only for development use, not for production!* | `True`                                                                                                               |
| DEV_USE_PREDEFINED_USER      | Set this to `True`, if you want to use a predefined user. *Only for development use, not for production!*                 | `False`                                                                                                              |
| DEV_FLASK_USERID             | Set the userId, which should be used, when `DEV_USE_PREDEFINED_USER` is `True`.                                           | test                                                                                                                 |


The `REDIRECTION_URL` and `OWNCLOUD_OAUTH_CLIENT_SECRET` fields can only be set up correctly, when you start up the corresponding oauth backend before. So you have to start the backends and configure the `.env` file properly. After this, you can stop everything and can use the receipts in the corresponding sections for use.

For easier access, you should start only the owncloud backend with the following commands and enable the `oauth2` and `rds` app and add a new oauth2 path in the settings, which is described [here](https://doc.owncloud.com/server/admin_manual/installation/apps_management_installation.html), [here](https://doc.owncloud.com/server/admin_manual/configuration/server/security/oauth2.html#installation) and [here](https://www.research-data-services.org/doc/impl/plugins/owncloud/).

```bash
docker-compose -f client/dev/docker-compose.yml up -d
```

Now open the url `http://localhost:8000` in your favourite browser and enable and setup all needed apps. For oauth, you will need one client for domain `http://localhost:9100/oidc-callback.html`, when you want to develope for OC Web. If you want to develope for standalone, you will need a client for domain `localhost:8080`.
After this, you have all informations to configure the `.env` correctly. Now, you can continue with the setup.

Remind: If you delete all docker-resources (e.g. with `docker system prune --volumes`), you have to do all steps before again to get valid values for `.env` file.

### Client setup

Install all nodejs dependencies.
```bash
yarn --cwd client install
yarn --cwd client/dev/web install
```

Now, you have to configure the OC Web server
```bash
cp client/dev/web/config/config.json.sample-oc10 client/dev/web/config/config.json
vi client/dev/web/config/config.json
```

In the `config.json`, you have to specify your owncloud classic backend (in docker-compose specified with `localhost:8000`, you access it before in your browser) and set your clientId, which you generate previously in oauth2 app inside of your owncloud classic instance. This is also described [here](https://owncloud.dev/clients/web/backend-oc10/). When you want to change the config.php of the owncloud classic backend, you can get this done with `docker exec -it dev_owncloud_1 /bin/bash -c vi config/config.php`.

Beware: You have to change the port from `8080` to `8000` in the fields `url` and `authUrl`.
Then, you have to add our RDS application in `external_apps` field. Copy the following code snippet and add it to the array.

```javascript
{
    "id": "rds",
    "path": "http://localhost:8082/index.js",
    "config": {
        "url": "http://localhost:8080",
        "describo": "http://localhost:8090"
    }
},
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

**Beware: For development and production, you need access to a [working RDS instance](https://www.research-data-services.org/doc/getting-started/k8s/). For example through VPN with `openconnect` to an already existing one or use minikube for smaller test environments.**

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
