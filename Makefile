
HOST=csud-reservation.com
SSH_OPTIONS=-o 'StrictHostKeyChecking no'
SSH = ssh $(SSH_OPTIONS) root@$(HOST)
SERVER_DIR=~/csud-reservation
RSYNC_OPTIONS= -e 'ssh -o StrictHostKeyChecking=no'
RSYNC=rsync $(RSYNC_OPTIONS)

REMOTE_NGINX=$(SSH) docker exec nginxletsencrypt_nginx-proxy_1 

SSH_SERVER=$(SSH) cd $(SERVER_DIR) &&

init:
	cd vserver && make setup-docker

ssh:
	$(SSH)

push:
	$(RSYNC) -raz . root@www.csud-reservation.com:$(SERVER_DIR) --progress --exclude=.git --exclude=venv --exclude=__pycache__

server-up: push
	$(SSH) 'cd $(SERVER_DIR)/nginx-letsencrypt && docker-compose build && docker-compose up -d'
	$(SSH) 'cd $(SERVER_DIR) && docker-compose build && docker-compose -f docker-compose.yml -f docker-compose.sqlite.local.yml up -d'
server-down:
	$(SSH) 'cd $(SERVER_DIR) && docker-compose down'
	$(SSH) 'cd $(SERVER_DIR)/nginx-letsencrypt && docker-compose down'
initweb:
	$(SSH) 'cd $(SERVER_DIR) && docker-compose exec web python manage.py initdb'
	$(SSH) 'cd $(SERVER_DIR) && docker-compose exec web python manage.py load'

server-restart: server-down server-up

olddown:
	$(SSH) cd $(SERVER_DIR) && 
oldup:
oldrestart: down up


inspect-nginx-config:
	$(REMOTE_NGINX)  cat /etc/nginx/conf.d/default.conf
inspect-webapp:
	$(SSH) docker inspect csudreservation_web


ps:
	$(SSH) docker ps

webapp-shell:
	$(SSH_SERVER) 


local-up:
	docker-compose build
	docker-compose -f docker-compose.yml -f docker-compose.sqlite.local.yml up -d
local-down:
	docker-compose -f docker-compose.yml -f docker-compose.sqlite.local.yml down
local-restart: local-down local-up
up: local-up
down: local-down
restart: local-restart
