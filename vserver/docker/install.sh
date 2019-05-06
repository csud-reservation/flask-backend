#!/bin/sh

apt-get -y purge lxc-docker*
apt-get -y purge docker.io*

apt-get -y update
apt-get -y install apt-transport-https ca-certificates
apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
echo "deb https://apt.dockerproject.org/repo debian-jessie main" > /etc/apt/sources.list.d/docker.list

apt-get -y update
apt-get -y install docker-engine --allow-unauthenticated
service docker start

# curl https://raw.githubusercontent.com/docker/docker/master/contrib/completion/bash/docker -O ~/.docker-completion.sh '. ~/.docker-completion.sh' >> ~/.bash_rc
# curl https://raw.githubusercontent.com/docker/compose/$(docker-compose --version | awk 'NR==1{print $NF}')/contrib/completion/bash/docker-compose -O ~/.docker-compose-completion.sh '. ~/.docker-machine-completion.sh' >> ~/.bash_rc
# curl https://raw.githubusercontent.com/docker/machine/master/contrib/completion/bash/docker-machine.bash -O ~/.docker-machine-completion.sh '. ~/.docker-compose-completion.sh' >> ~/.bash_rc

