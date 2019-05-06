FROM debian:jessie-slim

# ARG version
# ENV BACKUP_BRANCH="$version"

RUN apt-get update
RUN apt-get install -y cron sqlite3 git
RUN apt-get install -y bash

# RUN pip install awscli

# TODO : j'aimerais bien une manière de pouvoir spécifier cette variable dans le
# docker-compose ou même dans une variable d'environnement ... 
ENV BACKUP_BRANCH staging-test

WORKDIR /backups

# cette commande contient une clé qui permet de ne pas saisir de mot de passe,
# c'est une sorte de jeton ... je ne sais plus trop d'où cela vient...
RUN git clone https://donnerc:53CU8t7DqabJjcZJYT27@bitbucket.org/donnerc/csud-reservation-backups.git /backups

# la logique n'est pas assez fine dans ces instructions. Le problème est qu'il
# faudrait créer la branche si elle n'existe pas mais faire un simple checkout
# si elle existe déjà ... Ce test est maintenant effectué lors de chaque
# sauvegarde dans le script dump-and-push.sh RUN echo branch ${BACKUP_BRANCH}
# RUN git checkout -b ${BACKUP_BRANCH}

WORKDIR /root

ADD crontab crontab_file.txt
ADD dump-and-push.sh /root/dump-and-push.sh
RUN chmod +x /root/dump-and-push.sh

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

RUN crontab crontab_file.txt


# Run the command on container startup
CMD cron && tail -f /var/log/cron.log