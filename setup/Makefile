ifneq (,$(wildcard ./.env))
    include .env
    export
endif

start:
	docker-compose up -d

build:
	docker-compose up -d --build

stop:
	docker-compose down

clean:
	docker-compose down --remove-orphans 
	docker-compose down --rmi all --volumes

CONFIG = $$CONFIG
install: start
	@echo "Not for production use!!! Or remove the oauth2 client by hand and create a new one and set all informations in docker-compose.yml"
	@echo "Wait for ownCloud installation completion."
	@while [ $(shell curl  -sw '%{http_code}' localhost) -gt 302 ]; do true; done;
	@docker exec -it owncloud_server /bin/bash -c "head -n -1 config/config.php > config.php"
	@docker exec -it owncloud_server /bin/bash -c "echo \"'web.baseUrl' => 'http://${OWNCLOUD_DOMAIN}/web', 'cors.allowed-domains' => ['http://${OWNCLOUD_DOMAIN}:9100','http://${OWNCLOUD_DOMAIN}:8008'],);\" >> config.php"
	@docker exec -it owncloud_server /bin/bash -c "cp config.php config/config.php"
	@docker exec -it owncloud_server /bin/bash -c "occ user:modify admin email ${ADMIN_MAIL}"
	@docker exec -it owncloud_server /bin/bash -c "occ market:install oauth2 && occ market:install web && occ app:enable oauth2 && occ app:enable rds"
	@docker exec -it owncloud_server /bin/bash -c "occ rds:set-oauthname web && occ rds:set-url ${RDS_URL}"
	@docker exec -it owncloud_server /bin/bash -c "occ oauth2:add-client web ${OWNCLOUD_OAUTH2_CLIENT_ID} ${OWNCLOUD_OAUTH2_CLIENT_SECRET} ${OWNCLOUD_OAUTH2_CLIENT_REDIRECT}"
	

