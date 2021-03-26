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

test:
	npm --prefix ./client test && cd server && pipenv run pytest

web:
	yarn --cwd ./client workspace web run build
	cp -ru ./client/packages/web/dist ./client/dev/web
	@tmux new-session -d -s ocis "cd ocis/ocis && OCIS_LOG_PRETTY=true OCIS_LOG_COLOR=true OCIS_LOG_LEVEL=DEBUG go run cmd/ocis/main.go server"\;\
		 split-window -h "yarn --cwd web serve"\;\
		 split-window -h "yarn --cwd extension serve"
	@echo "Wait 20s for server startup to kill web"
	@sleep 20
	@tmux new-session -d "cd ocis/ocis && go run cmd/ocis/main.go kill web"
	@echo "Done. Open https://localhost:9200 with your browser."
	@echo 'If you want to close the server, execute "make stop" and close everything.'

classic:
	yarn --cwd ./client workspace classic run build
	cp -ru ./client/packages/classic/dist ./client/packages/classic/php
	docker-compose -f client/dev/docker-compose.yml up -d
	tmux new-session -d -s classic "cd server && while true; do pipenv run python starter.py; done" \;

standalone:
	docker-compose -f client/dev/docker-compose.yml up -d
	tmux new-session -d -s standalone "cd client && while true; do yarn serve; done" \; split-window -h "cd server && while true; do pipenv run python starter.py; done" \;
	@echo Wait for 20 Seconds to boot everything up.
	@sleep 20
	docker exec -it dev_owncloud_1 /bin/bash -c "occ app:enable oauth2 && occ app:enable rds"
	@echo Start on http://localhost:8080

stop:
	docker-compose -f client/dev/docker-compose.yml down
	tmux kill-session -t ocis || true
	tmux kill-session -t classic || true
	tmux kill-session -t standalone || true