ifneq (,$(wildcard ./.env))
    include .env
    export
endif

ubuntu:
	sudo apt install -y curl unzip

fedora:
	sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
	sudo yum install -y curl unzip yum-utils docker-ce docker-ce-cli containerd.io

start:
	docker-compose up -d

stop:
	docker-compose down

install: start
	@curl https://github.com/Sciebo-RDS/RDS-Web/releases/latest/download/ocClassicPlugin.zip -o ocClassicPlugin.zip
	@unzip ocClassicPlugin.zip -d rds
	@docker cp ./rds owncloud_server:/var/www/owncloud/apps/rds
	@docker cp ./config.php owncloud_server:/var/www/owncloud/config.php
	@docker exec -it owncloud_server /bin/bash -c "cat $"<?php $" > config.php"
	@docker exec -it owncloud_server /bin/bash -c "php -r $"require('config/config.php'); $CONFIG=array_merge($CONFIG, array('web.baseUrl' => 'http://${OWNCLOUD_DOMAIN}:9100','cors.allowed-domains' => ['https://${OWNCLOUD_DOMAIN}:9100'])); file_put_contents("config.php", print_r($CONFIG, true), FILE_APPEND);$""
	@docker exec -it owncloud_server /bin/bash -c "cp config.php config/config.php"
	@docker exec -it owncloud_server /bin/bash -c "occ user:modify admin email ${ADMIN_MAIL}"
	@docker exec -it owncloud_server /bin/bash -c "occ market:install oauth2 && occ market:install web && occ app:enable oauth2 && occ app:enable rds"
	@docker exec -it owncloud_server /bin/bash -c "occ oauth2:add-client web ${OWNCLOUD_OAUTH2_CLIENT_ID} ${OWNCLOUD_OAUTH2_CLIENT_SECRET} ${OWNCLOUD_OAUTH2_CLIENT_REDIRECT} | true"
	

