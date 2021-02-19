install:
	apt install gettext
	npm install

l10n-compile:
	 npm run localize-compile 
	
l10n-extract:
	npm run localize-extract

flask:
	pipenv shell
	FLASK_APP=server.py flask run

socket:
	pipenv run python websocket.py

lint:
	npm run lint
	pipenv run black .

build:
	npm run build

test:
	tmux new-session "npm run serve" \; split-window -h "pipenv run python websocket.py" \;  
