import os


def get_page_access_token():
    token = 'EAABmWGMeZCQwBADig5fcJHPtYFhuQqGCwAWuHNbJzYyOKJfUZAGeqd8Yo2eqMEQ3ZCh8kDvsoKpB2t94ZC7MGNKnhMBzxo7LgqUSZCRlPSXQFPkKSw2jFX3ixQekurmKZB8Ewhqudi0CeXnyKVPZAnhQwAxrBiswC6aw7wnOIlmYQZDZD'
    # token = 'EAABmWGMeZCQwBANQEdVYnVEWb3hrXBYYkb9kJcUWQV9ksqSgZCZAkZARQZATNHHmYINpW2sVI5f4U4l3hn9LtWIOG91WtmGRg80uF9FUsRj6YCfvG0gcdXFBlWDItbcE4VQLYqOilTeppWUHALSKRTkdRDHCGzmYWRLDMikZAcuQZDZD'
    return os.environ.get('PAGE_ACCESS_TOKEN', token)


def get_verify_token():
    return os.environ.get('VERIFY_TOKEN', 'Very_Secret_Token')
