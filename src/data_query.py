import os
import logging
from typing import Dict, Any
from elasticsearch import Elasticsearch

# Index name in ES
index_name = 'nobel-prizes'

logging.basicConfig(format='%(levelname)s :: %(asctime)s :: %(message)s', datefmt='%Y-%m-%d %I:%M:%S')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def search(client: Any, index: str, query: Dict, size: int = 500):
    ret = client.search(index=index, body=query, size=size)
    return ret['hits']['hits']


if __name__ == "__main__":
    # Initialize elasticsearch client
    esClient = Elasticsearch(hosts=[os.environ['es_node1'], os.environ['es_node2']])
    logger.info(esClient.cluster.health())

    # Fetch all first 20 chemistry prizes sorted by year
    query = {
        "sort": {
            "year": {"order": "asc"}
        },
        "query": {
            "match": {
                "category": "chemistry"
            }
        }
    }
    res = search(esClient, index_name, query, size=20)
    for entry in res:
        logger.info(entry['_source'])
