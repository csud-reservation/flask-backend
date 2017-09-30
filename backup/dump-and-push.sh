#!/bin/bash

cd /backups 
sqlite3 /sqlite-data/data.sqlite .dump > dump.sql 
git add dump.sql
git commit -m "auto backup $(date +%d-%m-%Y-%H:%M)" 
git push origin $BACKUP_BRANCH