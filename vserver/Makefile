SSH_OPTIONS=-o 'StrictHostKeyChecking no'
SSH_ROOT = ssh $(SSH_OPTIONS) root@$(HOST)
RSYNC_OPTIONS= -e 'ssh -o StrictHostKeyChecking=no'
RSYNC=rsync $(RSYNC_OPTIONS)
SSH = $(SSH_ROOT) 
ROOT = root@$(HOST)
SYNC = rsync -raz --delete --progress $(ROOT)

DOCKER_COMPOSE_VERSION = 1.15.0

init: upgrade
	$(SSH) apt-get -y install curl rsync git build-essential

setup-docker: init put-setup
	cat docker/install.sh | $(SSH) sh
	$(SSH) 'curl -L https://github.com/docker/compose/releases/download/$(DOCKER_COMPOSE_VERSION)/docker-compose-`uname -s`-`uname -m` > /usr/bin/docker-compose && chmod +x /usr/bin/docker-compose'	

# pour pousser les modifications locales sur le serveur
put-setup:
	$(RSYNC) -raz * root@$(HOST):/root/setup/ --progress --delete

ssh-root:
	$(SSH)

ssh: ssh-root

setup-ssh:
	cat ~/.ssh/id_rsa.pub | $(SSH) 'touch .ssh/authorized_keys && cat >> .ssh/authorized_keys'

clean-ssh:
	rm -f ~/.ssh/known_hosts

upgrade:
	$(SSH) apt-get update -y
	$(SSH) apt-get upgrade -y

halt:
	$(SSH) 'halt && sleep 5s && ping $(HOST)'

reboot:
	$(SSH) reboot
	sleep 2s && ping $(HOST)
	sleep 20s && ping $(HOST)

