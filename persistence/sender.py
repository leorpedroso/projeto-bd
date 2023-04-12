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
                    "last_changed.keyword": {
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


    def get_all_indices(self):
        return self.client.indices.get_alias(index="*")
 

    def post_champ_indexes(self, champ_names):
        print('Posting champ names index...')
        self.client.index(
            index='champ_names',
            refresh='wait_for',
            document={'names': champ_names}
        )
        print('Done!')


    def get_champ_indexes(self):
        res = self.client.search(
            index='champ_names',
            body={
                'size': 10000,
                'query': {
                    'match_all': {}
                }
            }
        )

        return res['hits']['hits'][0]['_source']['names']


    # assumes champ_name index exists in elastic
    def get_champ_info(self, champ_name):
        res = self.client.search(
            index = champ_name,
            body={
                'size': 1,
                'query': {
                    'match_all': {}
                }
            }
        )
        
        return res['hits']['hits'][0]['_source']


    def populate_info_index(self):
        # for champ in champs
        #   get champ from es
        #   infos[att].append((value, champ))
        filter_out = ['name', 'last_changed', 'abilities', 'alias', 'species', 'occupation', 'quote']
        numeric_att = ['health', 'health_regen', 'resource', 'resource_regen', 'armor', 'magic_resist',
                       'attack_damage', 'mov_speed', 'range', 'store_price_be', 'store_price_rp']

        infos = {}
        champs = self.get_champ_indexes()
        for champ in champs:
            info = self.get_champ_info(champ.lower())
            for att in info:
                if att in filter_out:
                    continue

                value = info[att]

                if not value:
                    continue

                if att not in infos:
                    infos[att] = []

                if type(value) == list:
                    infos[att] += value                   
                else:
                    if att in numeric_att:
                        value = float(value)

                    infos[att].append(value)

        for info in infos:
            infos[info].sort()
            if info in numeric_att or info == 'release_date':
                infos[info] = [infos[info][0], infos[info][-1]]
            else:
                infos[info] = list(set(infos[info]))

        print(infos)
        return infos

    def post_info_index(self):
        print('Posting info index...')
        infos = self.populate_info_index()

        self.client.index(
            index='attributes',
            document=infos
        )

        print('Done!')


    def get_attributes(self):
        res = self.client.search(
            index='attributes',
            body={
                'query': {
                    'match_all': {}
                }
            }
        )

        return res['hits']['hits'][0]['_source']

    
    def get_champ_from_att(self, attribute, value):
        champs = self.get_champ_indexes()
        for champ in champs:
            info = self.get_champ_info(champ.lower())
            # print(info['name'], info[attribute])
            # print(value)
            if info[attribute] and (float(info[attribute]) == value):
                return info['name']
 
