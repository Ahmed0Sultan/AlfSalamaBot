import os


def get_page_access_token():
    token = 'EAABZCmSBgOJUBAIWVw0cDFIBTryNoIIxKN1HaTy4rxg7lIATKn7zpcjO5wfBFk0TCV2tGZApsYM6eJxgB7DbiJShBrwWi64kiWchKUGis57sPr8OikR46ZCLJdAMAl3UkumrCRPp0cbQaSLvZBmZBLsqHlJRDdJvCrBmJS7pBmQZDZD'
    return os.environ.get('PAGE_ACCESS_TOKEN', token)


def get_verify_token():
    return os.environ.get('VERIFY_TOKEN', 'Very_Secret_Token')
