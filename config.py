import os


def get_page_access_token():
    token = 'EAABZCmSBgOJUBAJ2OaPxb074LsPiTJkDLyV1QSufjTrjdptdHGu35Wb05ZCP7dr0aFsWO9lfZBchOjbbKYS7ENeCWKtafDM089oShsYyw1SkPxMKzIA8zLtLcCBFQnf5YHpKBWVCZB20xiYdVjRoG5BoyMFv4tRyZAxG57kL9VgZDZD'
    return os.environ.get('PAGE_ACCESS_TOKEN', token)


def get_verify_token():
    return os.environ.get('VERIFY_TOKEN', 'Very_Secret_Token')
