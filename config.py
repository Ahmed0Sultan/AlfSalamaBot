import os


def get_page_access_token():
    token = 'EAABmWGMeZCQwBAEF7XykkZClaHLFmBDOR89DyJhFRG6pxwigZCL2NCS74r1WvooAcpV4dueiJsSUgPr3OyJGzyUb0ZCvDr5RAWjOlb8K0cyVNHjHKUMOgKGZAchkYCR0OxlBWApxMNpZBKkFGlcu5qfJucWsSuGOHofmusUvEPOAZDZD'
    return os.environ.get('PAGE_ACCESS_TOKEN', token)


def get_verify_token():
    return os.environ.get('VERIFY_TOKEN', 'Very_Secret_Token')
