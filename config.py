import os


def get_page_access_token():
    token = 'EAABZCmSBgOJUBACJnsSG4bHZAqe0vPZA9mDUbeHzG0oclgJbVmVQMZC9OmmJetdedASdJZBKw8CZCxR5gUAXXZBrofM5jbbJJcQCMc9S4HeyIsRuXHENcwr12ALLUiufWs0IMAOQthQWXOXk3fCk3SkWkqCYSD47lWIsqB7XaMk7wG3JNcZB3ZBZBI'
    return os.environ.get('PAGE_ACCESS_TOKEN', token)


def get_verify_token():
    return os.environ.get('VERIFY_TOKEN', 'Very_Secret_Token')
