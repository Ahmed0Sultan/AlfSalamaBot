import os


def get_page_access_token():
    token = 'EAABmWGMeZCQwBADig5fcJHPtYFhuQqGCwAWuHNbJzYyOKJfUZAGeqd8Yo2eqMEQ3ZCh8kDvsoKpB2t94ZC7MGNKnhMBzxo7LgqUSZCRlPSXQFPkKSw2jFX3ixQekurmKZB8Ewhqudi0CeXnyKVPZAnhQwAxrBiswC6aw7wnOIlmYQZDZD'
    return os.environ.get('PAGE_ACCESS_TOKEN', token)


def get_verify_token():
    return os.environ.get('VERIFY_TOKEN', 'Very_Secret_Token')
