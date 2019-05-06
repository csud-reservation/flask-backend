#!/bin/bash

cd /backups 
sqlite3 /sqlite-data/data.sqlite .dump > dump.sql 

# checkout branch if exists ; create branch if it doesn't exist
git show-ref --verify --quiet refs/heads/$BACKUP_BRANCH
if [ "$?" -eq "0"]; then
    git checkout $BACKUP_BRANCH
else
    git checkout -b $BACKUP_BRANCH
fi
git add dump.sql
git commit -m "auto backup $(date +%d-%m-%Y-%H:%M)" 
git push -u origin $BACKUP_BRANCH