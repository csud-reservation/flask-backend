#!/bin/sh

sudo apt-get purge lxc-docker*
sudo apt-get purge docker.io*

sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates
sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
sudo echo "deb https://apt.dockerproject.org/repo debian-jessie main" > /etc/apt/sources.list.d/docker.list
sudo apt-get update
sudo apt-cache policy docker-engine
sudo apt-get update
sudo apt-get install docker-engine
sudo service docker start

wget https://raw.githubusercontent.com/docker/docker/master/contrib/completion/bash/docker -O ~/.docker-completion.sh
wget https://raw.githubusercontent.com/docker/compose/$(docker-compose --version | awk 'NR==1{print $NF}')/contrib/completion/bash/docker-compose -O ~/.docker-compose-completion.sh
wget https://raw.githubusercontent.com/docker/machine/master/contrib/completion/bash/docker-machine.bash -O ~/.docker-machine-completion.sh
cat '. ~/.docker-completion.sh' >> ~/.bash_rc
cat '. ~/.docker-machine-completion.sh' >> ~/.bash_rc
cat '. ~/.docker-compose-completion.sh' >> ~/.bash_rc

