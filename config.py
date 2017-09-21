import os


def get_page_access_token():
    token = 'EAABmWGMeZCQwBAIWcjfiZCi4ZBT6khwb4sY7Nw5bLrrpZCaTW8DX6420C9NIEL9AqZAbK8OmZC5WezRn3KFrZC7i7UClyDo2HL7HElAVzddxaV60Ogoe67GAbxgK5Gp3NuZCiFeXDtBhT8XX97NUreFGNwwWCS7NY80jN2GmtuGOawZDZD'
    return os.environ.get('PAGE_ACCESS_TOKEN', token)


def get_verify_token():
    return os.environ.get('VERIFY_TOKEN', 'Very_Secret_Token')
