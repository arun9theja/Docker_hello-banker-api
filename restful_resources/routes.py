from restful_resources.account import AccountApi, AccountsDetailApi


def initialize_routes(api):
    api.add_resource(AccountApi, '/api/accounts')
    api.add_resource(AccountsDetailApi, '/api/accounts_detail')

