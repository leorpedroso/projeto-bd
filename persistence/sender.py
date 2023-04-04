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
        try:
            print(f'Verifying post {champ} to elastic')
            if not self.verify_post_to_elastic(champ, dict):
                return
            
            print(f'Posting {champ} to elastic...')
            self.client.index(
                index=champ.lower(),
                document=dict
            )
            print('Done!')
        
        except Exception as e:
            print(f'Failed to post {champ} data')
            print(e)

    
    def get_most_recent_version(self, champ):
        if not self.check_index_exists(champ.lower()):
            return
        
        res = self.client.search(
            index=champ,
            body={
                'size': 10000,
                'query': {
                    'match_all': {}
                }
            }
        )

        if 'last_changed' in res['hits']['hits'][0]['_source']:
            return res['hits']['hits'][0]['_source']['last_changed']
        