
HOST=csud-reservation.com
SSH_OPTIONS=-o 'StrictHostKeyChecking no'
SSH = ssh $(SSH_OPTIONS) root@$(HOST)
SERVER_DIR=~/csud-reservation
RSYNC_OPTIONS= -e 'ssh -o StrictHostKeyChecking=no'
RSYNC=rsync $(RSYNC_OPTIONS)



init:
	cd vserver && make setup-docker

production: init
	$(RSYNC) -raz . root@www.csud-reservation.com:$(SERVER_DIR) --progress --exclude=.git --exclude=venv --exclude=__pycache__
	$(SSH) 'cd $(SERVER_DIR) && docker-compose up -d'
	$(SSH) 'cd $(SERVER_DIR)/nginx-letsencrypt && docker-compose up -d'

ssh:
	$(SSH)

up: production
	$(SSH) docker run -d --expose=8080 --env VIRTUAL_HOST=www.csud-reservation.com --env LETSENCRYPT_HOST=www.csud-reservation.com --env LETSENCRYPT_EMAIL=cedonner@gmail.com --env C9_HOSTNAME=https://www.csud-reservation.com --env C9_IP=0.0.0.0 --env C9_PORT=8080 csudreservation_web