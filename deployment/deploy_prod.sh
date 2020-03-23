#!/bin/sh

ssh -o StrictHostKeyChecking=no -T root@206.189.212.117 <<EOF
  cd /srv/mat-api
  git pull
  pwd
  exit
EOF