
HOST=csud-reservation.com
SSH = ssh root@$(HOST)
SERVER_DIR=csud-reservation


production:b
	rsync -raz . root@www.csud-reservation.com:~/$(SERVER_DIR) --progress --exclude=.git
	$(SSH) cd $(SERVER_DIR) && docker-compose up -d

ssh:
	$(SSH)

up:
	$(SSH) docker run --expose=8080 --env VIRTUAL_HOST=www.csud-reservation.com --env LETSENCRYPT_HOST=www.csud-reservation.com --env LETSENCRYPT_EMAIL=cedonner@gmail.com --env C9_HOSTNAME=https://www.csud-reservation.com --env C9_IP=0.0.0.0 --env C9_PORT=8080 -it csudreservation_web