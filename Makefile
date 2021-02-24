install:
	apt install gettext
	npm install
	npm install --only=dev

l10n-compile:
	 npm run localize-compile 
	
l10n-extract:
	npm run localize-extract

flask:
	pipenv shell
	FLASK_APP=server.py flask run

socket:
	cd server && pipenv run python websocket.py

lint:
	npm run lint
	pipenv run black .

build:
	npm run build

hotreload:
	tmux new-session "npm run serve" \; split-window -h "cd server && pipenv run python websocket.py" \;  

test:
	npm test && cd server && pipenv run pytest
