docker rm -f uploader
docker image rm uploader:1

docker build --tag uploader:1 .
docker run --name uploader -p 8094:8094 -d uploader:1 