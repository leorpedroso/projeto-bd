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


    def get_all_indices(self):
        return self.client.indices.get_alias(index="*")
    
# qiyana
# vladimir
# jayce
# janna
# kalista
# reksai
# irelia
# lux
# azir
# evelynn
# maokai
# .apm-custom-link
# aatrox
# .kibana_task_manager_8.6.2_001
# rengar
# leo
# pyke
# nocturne
# brand
# zac
# masteryi
# xayah
# jax
# darius
# teemo
# twistedfate
# quinn
# talon
# draven
# katarina
# annie
# tahmkench
# graves
# sona
# zilean
# rakan
# yorick
# poppy
# leesin
# milio
# wukong
# sejuani
# tristana
# neeko
# caitlyn
# singed
# garen
# heimerdinger
# nidalee
# karma
# leblanc
# twitch
# kled1
# sett
# gnar
# leona
# urgot
# viktor
# fizz
# kaisa
# .security-7
# gragas
# alistar
# volibear
# yone
# anivia
# jinx
# renataglasc
# khazix
# seraphine
# riven
# sion
# ashe
# nasus
# ryze
# blitzcrank
# malphite
# .kibana_security_session_1
# taliyah
# aurelionsol
# senna
# shen
# kayle
# sivir
# yasuo
# ezreal
# zyra
# zed
# hecarim
# trundle
# .security-profile-8
# kennen
# zeri
# pantheon
# diana
# shaco
# bard
# renekton
# galio
# ekko
# shyvana
# xinzhao
# .apm-agent-configuration
# kassadin
# lissandra
# vex
# gwen
# varus
# nautilus
# warwick
# drmundo
# soraka
# ahri
# vi
# chogath
# elise
# fiddlesticks
# amumu
# nami
# akali
# rumble
# missfortune
# corki
# velkoz
# .kibana_8.6.2_001
# rell
# gangplank
# nilah
# aphelios
# belveth
# vayne
# viego
# lillia
# tryndamere
# zoe
# jhin
# syndra
# karthus
# yuumi
# cassiopeia
# orianna
# ornn
# kayn
# kindred
# xerath
# thresh
# ksante
# samira
# udyr
# lulu
# veigar
# illaoi
# kogmaw
# mordekaiser
# ivern
# camille
# ziggs
# swain
# taric
# akshan
# braum
# fiora
# sylas
# lucian
# malzahar
# olaf
# morgana
# jarvaniv
# .kibana-event-log-8.6.2-000001
# nunu
# skarner
# rammus


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
        #pro aatrox retorna isso

#         {
#           "name": "Aatrox",
#           "last_changed": "V13.5",
#           "health": "650",
#           "resource": null,
#           "health_regen": "3",
#           "resource_regen": null,
#           "armor": "38",
#           "magic_resist": "32",
#           "attack_damage": "60",
#           "mov_speed": "345",
#           "range": "175",
#           "release_date": [
#             "2013-06-13"
#           ],
#           "class": [
#             "Juggernaut"
#           ],
#           "position": [
#             "Top",
#             "Middle"
#           ],
#           "range_type": [
#             "Melee"
#           ],
#           "adaptive_type": [
#             "Physical"
#           ],
#           "crit_damage": "175%",
#           "store_price_be": "4800",
#           "store_price_rp": "880",
#           "abilities": [
#             {
#               "name": "Deathbringer Stance",
#               "description": """INNATE - Periodically, The Champion empowers his next basic attack to gain  50 bonus range and deal bonus physical damage equal to 4% − 10% (based on level) of the target's maximum health, capped at 100 against  monsters.
# The Champion  heals for 80% of the post-mitigation bonus damage dealt, reduced to 25% against  minions.
# Whenever The Champion hits at least one enemy  champion or large  monster with a basic attack  on-hit or an ability, the  cooldown of Deathbringer Stance is reduced by 2 seconds, modified to 4 if he hits with the Sweetspot of  The Darkin Blade.
# """
#             },
#             {
#               "name": "The Darkin Blade",
#               "description": """ACTIVE - The Champion can activate The Darkin Blade three times before the ability goes on cooldown, with a 1 second static cooldown between casts. If The Champion does not recast the ability within 4 seconds of the previous cast, it goes on cooldown.
# The Champion performs a strike with his greatsword for each of the three casts, dealing physical damage to enemies hit within an area. Enemies hit within a Sweetspot of the area take 60% bonus damage and also  knocked up for 0.25 seconds. Each subsequent cast increases The Darkin Blade's damage by 25%.
# FIRST CAST - The Champion's first strike affects a 625 × 180-unit rectangular area in the target direction, with him centered on the back line and the Sweetspot at the farthest edge.
# SECOND CAST - The Champion's second strike affects a trapezoidal area in the target direction, with the Sweetspot at the farthest edge. The hitbox begins 100-units behind The Champion and extends 475-units in front of him, measuring between 300 and 500-units wide from behind to in front.
# THIRD CAST - The Champion's third strike affects a 300-radius circular area centered on a target location that is 200 units in front of him, with a 180-radius Sweetspot within.
# The Darkin Blade deals 55% damage against  minions, and the  knock up duration from hitting the Sweetspot is doubled to 0.5 seconds against  monsters.
# """
#             },
#             {
#               "name": "Infernal Chains",
#               "description": """ACTIVE - The Champion sends a chain in the target direction that deals physical damage to the first enemy hit, doubled against  minions, and  slowing them for 1.5 seconds.
# If this hits an enemy  champion or large  monster, a  tether is formed between the target and the ground beneath them for 1.5 seconds, during which they are  revealed.
# If the tether is not broken by the end of its duration, the target is dealt the same physical damage again and  pulled to the center of the area.
# """
#             },
#             {
#               "name": "Umbral Dash",
#               "description": """PASSIVE - The Champion  heals for a portion of the non- persistent post-mitigation damage he deals against enemy champions, increased during  World Ender.
# ACTIVE - The Champion  dashes in the target direction.
# Umbral Dash  resets The Champion's basic attack timer and can be cast during his other abilities without cancelling them and vice versa.
# """
#             },
#             {
#               "name": "World Ender",
#               "description": """ACTIVE - The Champion unleashes his true form for 10 seconds,  fearing nearby enemy  minions and  monsters for 3 seconds, during which they are gradually  slowed by up to 99% over the duration. He also gains  ghosting and  bonus movement speed that decays by 10% of the current bonus every 0.25 seconds, lasting until World Ender has ended.
# Whenever The Champion scores a champion  takedown, he extends the duration by 5 seconds and becomes unleashed again.
# During World Ender, The Champion gains  bonus attack damage and 5% increased size, and receives increased  self-healing from all sources.
# """
#             }
#           ],
#           "alias": [
#             "The Darkin Blade",
#             "Deathbringer",
#             "World Ender",
#             "God Killer",
#             "The Blade of Icathia"
#           ],
#           "species": [
#             "Darkin",
#             "God-Warrior",
#             "Human"
#           ],
#           "region": [
#             " Runeterra",
#             " Shurima"
#           ],
#           "occupation": [
#             "Warrior",
#             "Shuriman Guardian"
#           ],
#           "quote": "I must destroy even hope…"
#         }