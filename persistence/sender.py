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


    def post_champ_to_elastic(self, champ, dict):
        self.client.index(
            index=champ.lower(),
            document=dict
        )
            