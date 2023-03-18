champion_mapping = {
    "mappings": {
        "properties": {
            "last_changed": {"type": "date"},
            "base_hp": {"type": "short"},
            "hp_regen": {"type": "float"},
            "resource": {"type": "keyword"},
            "resource_regen": {"type": "float"},
            "armor": {"type": "float"},
            "magic_resist": {"type": "float"},
            "attack_damage": {"type": "float"},
            "crit_damage": {"type": "short"},
            "move_speed": {"type": "short"},
            "attack_range": {"type": "short"},
            "attack_speed": {"type": "short"},
            "release_date": {"type": "date"},
            "class": {"type": "keyword"},
            "position": {"type": "keyword"},
            "range_type": {"type": "keyword"},
            "store_price_be": {"type": "short"},
            "store_price_rp": {"type": "short"},
            "adaptive_type": {"type": "keyword"},
            "abilities": {"type": "nested"},
            "alias": {"type": "keyword"},
            "species": {"type": "keyword"},
            "region": {"type": "keyword"},
            "occupation": {"type": "keyword"},
            "quote": {"type": "text"},
        }
    }
}