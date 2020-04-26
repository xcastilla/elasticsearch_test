# Elasticsearch test
Repository to bring up an Elasticsearch cluster and run some test code against it.  
Requires `docker-compose`.

## Run Elasticsearch nodes
```
docker-compose up es_node1 es_node2
```

## Run test program
```
docker-compose up elastic-test
```

##  Bring down Elasticsearch nodes
```
docker-compose down
# Or if you want to delete the volumes
docker-compose down -v
```

## Linting and type checking
```
flake8 --config=.flake8 src/main.py
mypy --ignore-missing-import src/main.py
```