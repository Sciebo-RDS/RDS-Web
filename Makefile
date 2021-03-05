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
	FLASK_APP=starter.py flask run

socket:
	cd server && pipenv run python websocket.py

lint:
	npm run lint
	pipenv run black .

build:
	npm run build

hotreload:
	tmux new-session "cd client && while true; do npm run serve; done" \; split-window -h "cd server && while true; do pipenv run python starter.py; done" \;  

test:
	npm test && cd server && pipenv run pytest
