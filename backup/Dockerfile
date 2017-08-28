FROM python:3

RUN apt-get update && apt-get install -y cron

RUN pip install awscli

ADD crontab crontab_file.txt

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

RUN crontab crontab_file.txt


# Run the command on container startup
CMD cron && tail -f /var/log/cron.log