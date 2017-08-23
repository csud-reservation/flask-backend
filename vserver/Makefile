REMOTE = csud-reservation.com
SSH_ROOT = ssh root@$(REMOTE)
SSH = $(SSH_ROOT)
ROOT = root@$(REMOTE)
SYNC = rsync -raz --delete --progress $(ROOT)

DOCKER_COMPOSE_VERSION = 1.15.0

all: init nodejs docker chaj-docker oci

init: upgrade setup-docker
	$(SSH_ROOT) 'apt-get -y install curl rsync git build-essential'

setup-docker: put-setup
	cat docker/install.sh | $(SSH_ROOT) sh

setup-docker-compose:
	$(SSH_ROOT) 'curl -L https://github.com/docker/compose/releases/download/$(DOCKER_COMPOSE_VERSION)/docker-compose-`uname -s`-`uname -m` > /usr/bin/docker-compose && chmod +x /usr/bin/docker-compose'	

docker-machine: docker-machine-completion
	sudo curl -L https://github.com/docker/machine/releases/download/v0.6.0/docker-machine-`uname -s`-`uname -m` > /usr/local/bin/docker-machine && \
chmod +x /usr/local/bin/docker-machine

docker-machine-completion:
	# installation des scripts de complétion automatique
	sudo docker/setup-docker-machine.sh

# pour chercher ce qu'il y a sur le serveur et le mettre en local
# ATTENTION DANGER !!! ==> normalement, on fait toujours les modifs en local ...
get-setup: init
	rsync -raz root@$(REMOTE):/root/setup/* . --progress --delete

# pour pousser les modifications locales sur le serveur
put-setup:
	rsync -raz * root@$(REMOTE):/root/setup/ --progress --delete

ssh-root:
	$(SSH_ROOT)

ssh: ssh-root

ssh-setup:
	$(SSH_ROOT) ssh-keygen

ssh-setup-root: ssh-setup
	cat ~/.ssh/id_rsa.pub | ssh root@$(REMOTE) 'touch .ssh/authorized_keys && cat >> .ssh/authorized_keys'

clean-ssh:
	rm -f ~/.ssh/known_hosts

upgrade:
	$(SSH_ROOT) apt-get update
	$(SSH_ROOT) apt-get upgrade -y

halt:
	$(SSH_ROOT) 'halt && sleep 5s && ping $(REMOTE)'

reboot:
	$(SSH_ROOT) reboot
	sleep 2s && ping $(REMOTE)
	sleep 20s && ping $(REMOTE)

