FROM debian:jessie-slim

ARG version
ENV BACKUP_BRANCH="$version"

RUN apt-get update
RUN apt-get install -y cron sqlite3 git
RUN apt-get install -y bash

# RUN pip install awscli

# Commenté pour essayer de passer le paramètres version depuis les variables
# d'environnement (argument du Dockerfile) 

ENV BACKUP_BRANCH 2017-production

WORKDIR /backups
RUN git clone https://donnerc:53CU8t7DqabJjcZJYT27@bitbucket.org/donnerc/csud-reservation-backups.git /backups
RUN echo branch ${BACKUP_BRANCH}
RUN git checkout -b ${BACKUP_BRANCH}


WORKDIR /root

ADD crontab crontab_file.txt
ADD dump-and-push.sh /root/dump-and-push.sh
RUN chmod +x /root/dump-and-push.sh

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

RUN crontab crontab_file.txt


# Run the command on container startup
CMD cron && tail -f /var/log/cron.log