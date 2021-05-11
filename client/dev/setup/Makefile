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

clean:
	docker-compose down --remove-orphans 
	docker-compose down --rmi all --volumes

CONFIG = $$CONFIG
install: start
	@docker cp ../../packages/classic/php owncloud_server:/var/www/owncloud/apps/rds
	@docker exec -it owncloud_server /bin/bash -c "head -n -1 config/config.php > config.php"
	@docker exec -it owncloud_server /bin/bash -c "echo \"'web.baseUrl' => 'http://${OWNCLOUD_DOMAIN}:9100', 'cors.allowed-domains' => ['https://${OWNCLOUD_DOMAIN}:9100'],);\" >> config.php"
	@docker exec -it owncloud_server /bin/bash -c "cp config.php config/config.php"
	@docker exec -it owncloud_server /bin/bash -c "occ user:modify admin email ${ADMIN_MAIL}"
	@docker exec -it owncloud_server /bin/bash -c "occ market:install oauth2 && occ market:install web && occ app:enable oauth2 && occ app:enable rds"
	@docker exec -it owncloud_server /bin/bash -c "occ oauth2:add-client web ${OWNCLOUD_OAUTH2_CLIENT_ID} ${OWNCLOUD_OAUTH2_CLIENT_SECRET} ${OWNCLOUD_OAUTH2_CLIENT_REDIRECT} | true"
	

