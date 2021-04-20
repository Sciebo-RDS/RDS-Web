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

test:
	yarn --cwd ./client test && cd server && cd server && pipenv run pytest

web:
	docker-compose -f client/dev/docker-compose.yml up -d
	tmux new-session -d -s ocis "yarn --cwd ./client/dev/web serve"\;\
		 split-window -h "yarn --cwd ./client workspace @rds/web serve" || true
	tmux new-session -d -s standalone "cd client && while true; do yarn serve; done" \; split-window -h "cd server && while true; do pipenv run python starter.py; done" \; || true
	@echo "Open http://localhost:9100 with your browser."
	@echo 'If you want to close the server, execute "make stop" and close everything.'

ocis:
	@echo "This is currently not tested!"
	@echo "Cancel with ctrl+c"
	@sleep 5
	tmux new-session -d -s ocis "cd client/dev/ocis/ocis && OCIS_LOG_PRETTY=true OCIS_LOG_COLOR=true OCIS_LOG_LEVEL=DEBUG go run cmd/ocis/main.go server"\;\
		 split-window -h "yarn --cwd ./client/dev/web serve"\;\
		 split-window -h "yarn --cwd ./client workspace @rds/web serve"
	tmux new-session -d -s standalone "cd client && while true; do yarn serve; done" \; split-window -h "cd server && while true; do pipenv run python starter.py; done" \; || test
	@echo "Wait 20s for server startup to kill web"
	@sleep 20
	tmux new-session -d "cd client/dev/ocis/ocis && go run cmd/ocis/main.go kill web"
	@echo "Done. Open http://localhost:9200 with your browser."
	@echo 'If you want to close the server, execute "make stop" and close everything.'

classic: describo
	yarn --cwd ./client classic
	echo '$$(function () {' > ./client/packages/classic/php/js/app.js
	cat ./client/packages/classic/dist/js/app.js >> ./client/packages/classic/php/js/app.js
	echo "});" >> ./client/packages/classic/php/js/app.js
	docker-compose -f client/dev/docker-compose.yml up -d
	tmux new-session -d -s standalone "cd client && while true; do yarn serve; done" \; split-window -h "cd server && while true; do pipenv run python starter.py; done" \;
	@echo Wait for 20 Seconds to boot everything up.
	@sleep 20
	docker exec -it dev_owncloud_1 /bin/bash -c "occ app:enable oauth2 && occ app:enable rds"
	@echo Warning!!! You have to create a new oauth2 url and enter it in root .env file and configure RDS properly.
	@echo Start on http://localhost:8000

standalone:
	docker-compose -f client/dev/docker-compose.yml up -d
	tmux new-session -d -s standalone "cd client && while true; do yarn serve; done" \; split-window -h "cd server && while true; do pipenv run python starter.py; done" \;
	@echo Wait for 20 Seconds to boot everything up.
	@sleep 20
	@docker exec -it dev_owncloud_1 /bin/bash -c "occ app:enable oauth2 && occ app:enable rds"
	@echo Warning!!! You have to create a new oauth2 url and enter it in root .env file and configure RDS properly.
	@echo Start on http://localhost:8000

describo:
	docker-compose -f client/dev/describo-online/docker-compose.yml up -d

stop:
	docker-compose -f client/dev/docker-compose.yml down || true
	docker-compose -f client/dev/describo-online/docker-compose.yml down || true
	tmux kill-session -t ocis || true
	tmux kill-session -t classic || true
	tmux kill-session -t standalone || true
	sudo chown -R $(shell id -un):$(shell id -gn) client
