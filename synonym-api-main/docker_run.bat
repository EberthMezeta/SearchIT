docker rm -f synonym-api
docker image rm synonym:1

docker build --tag synonym:1 .
docker run --name synonym-api -p 8091:8091 -d synonym:1 

