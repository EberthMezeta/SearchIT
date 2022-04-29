docker rm -f solr-front
docker image rm solr-front:1

docker build --tag solr-front:1 .
docker run --name solr-front -p 8095:80 -d solr-front:1 

