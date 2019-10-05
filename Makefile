USER=root
REMOTE=$(USER)@$(HOST)
SSH_OPTIONS=-o 'StrictHostKeyChecking no'
SSH = ssh $(SSH_OPTIONS) root@$(HOST)
SERVER_DIR=~/csud-reservation
RSYNC_OPTIONS= -e 'ssh -o StrictHostKeyChecking=no'
RSYNC=rsync $(RSYNC_OPTIONS)
TIME = $(shell date +%Y-%m-%d_%Hh%M)

BACKUP_DIR=~/OneDrive/csud-reservation-backups

REMOTE_NGINX=$(SSH) docker exec nginxletsencrypt_nginx-proxy_1 

SSH_SERVER=$(SSH) cd $(SERVER_DIR) &&

init:
	cd vserver && make setup-docker

ssh:
	$(SSH)

# ces variables sont utilisées dans le fichier docker-compos.sqlite.local.yml
host.env.build:
	@if test -z "$(HOST)"; then echo "variable HOST not defined"; exit 1; fi
	rm -f host.env
	echo "C9_HOSTNAME=https://$(HOST)" >> host.env
	echo "VIRTUAL_HOST=$(HOST)" >> host.env
	echo "LETSENCRYPT_HOST=$(HOST)" >> host.env

# permet de savoir sur quelle branche du dépôt de backup on va travailler
backup.env.build:
	@if test -z "$(BRANCH)"; then echo "variable BRANCH not defined"; exit 1; fi
	echo "BRANCH=$(BRANCH)" > backup.env

push: host.env.build backup.env.build
	$(RSYNC) -raz . $(REMOTE):$(SERVER_DIR) --progress --exclude=.git --exclude=venv --exclude=ubuntu --exclude=__pycache__

# getbackup:
# 	$(SSH) tar -cjf backup.tar.bz2 csud-reservation/backup
# 	$(RSYNC) $(REMOTE):/root/backup.tar.bz2 .

sqlite-data-pull:
	$(SSH) docker cp csudreservation_backup_1:/sqlite-data/data.sqlite ./data.sqlite
	$(RSYNC) $(REMOTE):/root/data.sqlite ./backup/data/backup-$(TIME).sqlite
	cp -f ./backup/data/backup-$(TIME).sqlite data-dev.sqlite
	cp -f ./backup/data/backup-$(TIME).sqlite $(BACKUP_DIR)
sqlite-copy-local:
	cp -f data-dev.sqlite backup/data/data.sqlite
sqlite-data-push:
	$(RSYNC) ./backup/data/data.sqlite $(REMOTE):/root/data.sqlite --progress
	$(SSH) docker cp ./data.sqlite csudreservation_backup_1:/sqlite-data/data.sqlite
sqlite-push-local-data: sqlite-copy-local sqlite-data-push


ethz-push:
	$(RSYNC) -raz ~/ethz/* $(REMOTE):/root/ethz --progress --exclude=camtasia* --exclude=*-sources-DE


# get-ssh-config:
# 	$(RSYNC) -raz $(REMOTE):/root/.ssh ./backup/ssh --progress


# backup-up: push
# 	$(SSH) 'cd $(SERVER_DIR)/backup && docker-compose build && docker-compose up -d'
# backup-down:
# 	$(SSH) 'cd $(SERVER_DIR)/backup && docker-compose down -d'
# backup-restart: backup-down backup-up

server-up:
	$(SSH) 'cd $(SERVER_DIR)/nginx-letsencrypt && docker-compose build && docker-compose up -d'
	$(SSH) 'cd $(SERVER_DIR) && docker-compose build && docker-compose -f docker-compose.yml -f docker-compose.sqlite.local.yml up -d'
server-down:
	$(SSH) 'cd $(SERVER_DIR) && docker-compose down'
	$(SSH) 'cd $(SERVER_DIR)/nginx-letsencrypt && docker-compose down'
initweb:
	$(SSH) 'cd $(SERVER_DIR) && docker-compose exec web python manage.py initdb'
	$(SSH) 'cd $(SERVER_DIR) && docker-compose exec web python manage.py load'

server-restart: server-down server-up

inspect-nginx-config:
	$(REMOTE_NGINX)  cat /etc/nginx/conf.d/default.conf
inspect-webapp:
	$(SSH) docker inspect csudreservation_web

ps:
	$(SSH) docker ps

webapp-shell:
	$(SSH_SERVER) 

# gestion des backups 
dump-and-push: 
	# ne fonctionne pas à cause d'une offending key mais 'input device is not a TTY'
	# il faut se connecter manuellement sur le docker host ...
	# TODO : trouver un contournement
	$(SSH) docker exec -it csudreservation_backup_1 /root/dump-and-push.sh

