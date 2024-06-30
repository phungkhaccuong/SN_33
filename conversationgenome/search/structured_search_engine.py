import os

import bittensor as bt
from elasticsearch import Elasticsearch


class StructuredSearchEngine:
    def __init__(self):
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        self.init_indices()

    def init_indices(self):
        # Create the index
        index_name = 'conversations'
        if not self.es.indices.exists(index=index_name):
            bt.logging.info("creating index...", index_name)
            self.es.indices.create(
                index=index_name,
                body={
                    "mappings": {
                        "properties": {
                            "guid": {"type": "text"},
                            "participants": {"type": "keyword"},
                            "lines": {"type": "text"}
                        }
                    }
                }
            )

