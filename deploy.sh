#!/bin/sh

ssh -o StrictHostKeyChecking=no root@$DIGITAL_OCEAN_IP_ADDRESS << 'ENDSSH'
  cd /srv/mat-api
  export $(cat .env | xargs)
  docker login -u $CI_REGISTRY_USER -p $CI_JOB_TOKEN $CI_REGISTRY
  docker pull $image:web
  docker pull $image:nginx
  docker-compose -f docker-compose.prod.yml up -d
ENDSSH
