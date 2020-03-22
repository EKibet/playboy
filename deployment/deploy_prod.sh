#!/bin/sh

ssh root@206.189.212.117 <<EOF
  cd /srv/mat-api
  git pull
  exit
EOF