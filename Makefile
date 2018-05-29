
REMOTE=root@$(HOST)
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

host.env.build:
	rm -f host.env
	echo "C9_HOSTNAME=https://$(HOST)" >> host.env
	echo "VIRTUAL_HOST=$(HOST)" >> host.env
	echo "LETSENCRYPT_HOST=$(HOST)" >> host.env

push: host.env.build
	$(RSYNC) -raz . $(REMOTE):$(SERVER_DIR) --progress --exclude=.git --exclude=venv --exclude=__pycache__


sqlite-data-pull:
	$(SSH) docker cp csudreservation_backup_1:/sqlite-data/data.sqlite ./data.sqlite
	$(RSYNC) $(REMOTE):/root/data.sqlite ./backup/data/backup-$(date +%Y-%m-%d_%H:%M).sqlite


getbackup:
	$(SSH) tar -cjf backup.tar.bz2 csud-reservation/backup
	$(RSYNC) $(REMOTE):/root/backup.tar.bz2 .

sqlite-data-push:
	$(RSYNC) ./backup/data.sqlite $(REMOTE):/root/data.sqlite --progress
	$(SSH) docker cp ./data.sqlite csudreservation_backup_1:/sqlite-data/data.sqlite

get-ssh-config:
	$(RSYNC) -raz $(REMOTE):/root/.ssh ./backup/ssh --progress





backup-up: push
	$(SSH) 'cd $(SERVER_DIR)/backup && docker-compose build && docker-compose up -d'
backup-down:
	$(SSH) 'cd $(SERVER_DIR)/backup && docker-compose down -d'
backup-restart: backup-down backup-up

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


# gestion des backups 
push-dumps: 
	# ne fonctionne pas à cause d'une offending key mais 'input device is not a TTY'
	# il faut se connecter manuellement sur le docker host ...
	# TODO : trouver un contournement
	$(SSH) docker exec -it csudreservation_backup_1 /root/dump-and-push.sh

