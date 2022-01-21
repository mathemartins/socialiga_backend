aws cloudformation create-stack --stack-name socialigastack-dev --capabilities CAPABILITY_IAM --template-body file://$PWD/socialiga_fullstack.yml

docker build -t socialiga-django .
docker image tag socialiga-django mathemartins/socialiga-django
docker image push mathemartins/socialiga-django

export DOCKER_HOST=tcp://44.233.10.84:2375
docker-compose -f docker-compose.yml run backend python /var/projects/socialiga/manage.py collectstatic
docker-compose -f docker-compose.yml run backend python /var/projects/socialiga/manage.py migrate
docker-compose -f docker-compose.yml up -d
docker-compose -f docker-compose.yml down -v --rmi all