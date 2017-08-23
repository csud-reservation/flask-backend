#!/bin/sh

for file in docker-machine-prompt.bash docker-machine-wrapper.bash	docker-machine.bash
do
  sudo curl https://raw.githubusercontent.com/docker/machine/master/contrib/completion/bash/$file > /etc/bash_completion.d/$file
done
