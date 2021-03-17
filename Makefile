install:
	apt install gettext
	cd client
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
	npm --prefix ./client run build

buildoc:
	sudo chown physicx:physicx owncloud/classic -R
	npm --prefix ./client run owncloud
	echo '$$(function () {' > owncloud/classic/js/app.js
	cat client/dist/js/app.js >> owncloud/classic/js/app.js
	cat client/dist/css/app.css >> owncloud/classic/css/app.css
	echo "});" >> owncloud/classic/js/app.js

hotreload:
	tmux new-session "cd client && while true; do npm run serve; done" \; split-window -h "cd server && while true; do pipenv run python starter.py; done" \;  

test:
	npm --prefix ./client test && cd server && pipenv run pytest

dev:
	sudo chown physicx:physicx owncloud/classic -R
	echo '$$(function () {' > owncloud/classic/js/app.js
	cat client/dist/js/app.js >> owncloud/classic/js/app.js
	cat client/dist/css/app.css >> owncloud/classic/css/app.css
	echo "});" >> owncloud/classic/js/app.js
	docker-compose -f owncloud/classic/docker-compose.yml up && sudo chown physicx:physicx owncloud/classic -R