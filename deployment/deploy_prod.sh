#!/bin/sh

sshpass -p 'TMProject123' ssh -o StrictHostKeyChecking=no -T root@206.189.212.117 <<EOF
  cd /srv/mat-api
  pwd
  exit
EOF