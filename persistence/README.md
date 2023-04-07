

pra rodar:
docker start elasticsearch 
docker start kibana

localhost:9200
localhost:5601

usuario e senha no .env

Passo a passo para rodar o elastic (requer Docker)

https://www.elastic.co/guide/en/elasticsearch/reference/current/run-elasticsearch-locally.html#_start_elasticsearch


`docker network create elastic`

`docker pull docker.elastic.co/elasticsearch/elasticsearch:8.6.2`

`docker run --name elasticsearch --net elastic -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -t docker.elastic.co/elasticsearch/elasticsearch:8.6.2`

`docker pull docker.elastic.co/kibana/kibana:8.6.2`

`docker run --name kibana --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:8.6.2`

