from restful_resources.account import AccountsApi


def initialize_routes(api):
    api.add_resource(AccountsApi, '/api/accounts')
