import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

class Elastic:

    def __init__(self):
        self.client = None

    def connect(self):
        load_dotenv()
        ELASTIC_USER = os.getenv('ELASTIC_USER')
        ELASTIC_PASS = os.getenv('ELASTIC_PASS')

        self.client = Elasticsearch(
            "https://localhost:9200",
            basic_auth=(ELASTIC_USER, ELASTIC_PASS),
            verify_certs=False
        )

    def check_index_exists(self, index):
        return self.client.indices.exists(index=index)
    

    def check_champ_version_exists(self, index, doc):
        res = self.client.search(
            index=index,
            query= {
                "term": {
                    "last_changed": {
                        "value": doc["last_changed"]
                    }
                }
            }
        )

        return res['hits']['total']['value'] > 0

    def verify_post_to_elastic(self, champ, dict):
        return (not self.check_index_exists(champ)) or (not self.check_champ_version_exists(champ, dict))
            

    def post_champ_to_elastic(self, champ, dict):
        print(f'Verifying post {champ} to elastic')
        if not self.verify_post_to_elastic(champ, dict):
            return
        
        print(f'Posting {champ} to elastic...')
        self.client.index(
            index=champ.lower(),
            document=dict
        )
        print('Done!')
            