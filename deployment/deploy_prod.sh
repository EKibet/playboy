#!/bin/sh

sshpass -p 'TMProject123' ssh -T root@206.189.212.117 <<EOF
  cd /srv/mat-api
  exit
EOF