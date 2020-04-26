import os
import urllib.error
from urllib.request import urlopen
import json
import logging
from typing import Optional, Dict, Any
from elasticsearch import Elasticsearch
from tqdm import tqdm

# Nobel prize data stored in json
URL = 'http://api.nobelprize.org/v1/prize.json'
# Index name in ES
index_name = 'nobel-prizes'

logging.basicConfig(format='%(levelname)s :: %(asctime)s :: %(message)s', datefmt='%Y-%m-%d %I:%M:%S')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def fetch_data(url: str) -> Optional[Dict]:
    try:
        with urlopen(url) as fd:
            dataset = json.loads(fd.read())
    except urllib.error.HTTPError:
        logger.error('Dataset couldn\'t be fetched')
        return None
    return dataset['prizes']


def insert(client: Any, index: str, dataset: Dict) -> None:
    logger.info('Inserting data...')
    for item in tqdm(dataset):
        client.index(index=index, doc_type="external", body=item)


def search(client: Any, index: str, query: Dict, size: int = 500):
    ret = client.search(index=index, body=query, size=size)
    return ret['hits']['hits']


if __name__ == "__main__":
    # Get json sample data
    dataset = fetch_data(URL)
    if dataset is None:
        exit()

    # Initialize elasticsearch client
    esClient = Elasticsearch(hosts=[os.environ['es_node1'], os.environ['es_node2']])
    logger.info(esClient.cluster.health())

    # Insert data to elastic search
    insert(esClient, index_name, dataset)

    # Update index to make sortable by year
    body = {
        "properties": {
            "year": {
                "type": "text",
                "fielddata": True
            }
        }
    }
    esClient.indices.put_mapping(index=index_name, body=body)

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
