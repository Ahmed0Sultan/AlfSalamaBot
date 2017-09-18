import os


def get_page_access_token():
    token = 'EAABZCmSBgOJUBAKW9Wzvqf7vDrXGR8wpYyEryFDJpTyW37BytcM3KMc3Ft6DI7rPjCJO0ZBExRwdeoZADlFGSXGGoVVLMQGff60ZBdiSNm6NgwK6mRFhIlXy4wAN4UJt0CJpJkAmWSlHCyFT9FOarNZAa1TElZCxwjJwo5WkmZBzAZDZD'
    return os.environ.get('PAGE_ACCESS_TOKEN', token)


def get_verify_token():
    return os.environ.get('VERIFY_TOKEN', 'Very_Secret_Token')
