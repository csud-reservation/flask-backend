#!/bin/sh

# apt-get -y purge lxc-docker*
# apt-get -y purge docker.io*

apt-get -y update
apt-get -y install apt-transport-https ca-certificates curl software-properties-common gnupg2
curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"


apt-get -y update
apt-get -y install docker-ce
systemctl status docker
docker -v

# curl https://raw.githubusercontent.com/docker/docker/master/contrib/completion/bash/docker -O ~/.docker-completion.sh '. ~/.docker-completion.sh' >> ~/.bash_rc
# curl https://raw.githubusercontent.com/docker/compose/$(docker-compose --version | awk 'NR==1{print $NF}')/contrib/completion/bash/docker-compose -O ~/.docker-compose-completion.sh '. ~/.docker-machine-completion.sh' >> ~/.bash_rc
# curl https://raw.githubusercontent.com/docker/machine/master/contrib/completion/bash/docker-machine.bash -O ~/.docker-machine-completion.sh '. ~/.docker-compose-completion.sh' >> ~/.bash_rc

