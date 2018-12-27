SSH_OPTIONS=-o 'StrictHostKeyChecking no'
SSH_ROOT = ssh $(SSH_OPTIONS) root@$(HOST)
RSYNC_OPTIONS= -e 'ssh -o StrictHostKeyChecking=no'
RSYNC=rsync $(RSYNC_OPTIONS)
SSH = $(SSH_ROOT) 
ROOT = root@$(HOST)
SYNC = rsync -raz --delete --progress $(ROOT)

DOCKER_COMPOSE_VERSION = 1.15.0

init: upgrade
	$(SSH) apt-get -y install curl rsync git build-essential --force-yes --fix-missing

setup-docker: init
	cat docker/install.sh | $(SSH) sh
	$(SSH) 'curl -L https://github.com/docker/compose/releases/download/$(DOCKER_COMPOSE_VERSION)/docker-compose-`uname -s`-`uname -m` > /usr/bin/docker-compose && chmod +x /usr/bin/docker-compose'	

# pour pousser les modifications locales sur le serveur
put-setup:
	$(RSYNC) -raz * root@$(HOST):/root/setup/ --progress --delete

ssh-root:
	$(SSH)

ssh: ssh-root

ssh-register-public-key:
	cat ~/.ssh/id_rsa.pub | $(SSH) 'cat >> .ssh/authorized_keys'

setup-ssh:
	$(SSH) 'mkdir .ssh && touch .ssh/authorized_keys'

clean-ssh:
	rm -f ~/.ssh/known_hosts

upgrade:
	$(SSH) apt-get update -y --force-yes
	$(SSH) apt-get upgrade -y --force-yes --fix-missing

halt:
	$(SSH) 'halt && sleep 5s && ping $(HOST)'

reboot:
	$(SSH) reboot
	sleep 2s && ping $(HOST)
	sleep 20s && ping $(HOST)

# nécessaire de mettre à jour plusieurs fois le DNS sur la machine de test Hyper-V
update-dns:
	$(SSH) 'echo "nameserver 8.8.8.8" >> /etc/resolv.conf && service networking restart'