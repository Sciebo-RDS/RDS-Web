install:
	apt install gettext
	cd client
	npm install -g yarn
	npm --prefix ./client install
	npm --prefix ./client install --only=dev

l10n-compile:
	npm --prefix ./client run localize-compile 
	
l10n-extract:
	npm --prefix ./client run localize-extract

flask:
	cd server
	pipenv shell
	FLASK_APP=starter.py flask run

socket:
	cd server && pipenv run python websocket.py

lint:
	npm --prefix ./client run lint
	pipenv run black .

build:
	yarn --prefix ./client workspaces build

buildweb:
	npm --prefix ./client run ocweb
	cat client/dist/app.css >> client/packages/web/src/app.css
	cat client/dist/app.umd.min.js >> client/packages/web/src/app.umd.min.js

buildoc:
	sudo chown physicx:physicx client/packages/classic -R
	npm --prefix ./client run occlassic
	echo '$$(function () {' > client/packages/classic/js/app.js
	cat client/packages/classic/dist/js/app.js >> client/packages/classic/js/app.js
	cat client/dist/css/app.css >> client/packages/classic/css/app.css
	echo "});" >> owncloud/classic/js/app.js

hotreload:
	tmux new-session "cd client && while true; do yarn workspace codebase run serve; done" \; split-window -h "cd server && while true; do pipenv run python starter.py; done" \;  

test:
	npm --cwd ./client test && cd server && pipenv run pytest

dev:
	docker-compose -f client/dev/docker-compose.yml up