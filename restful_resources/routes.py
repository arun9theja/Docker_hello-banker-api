from restful_resources.account import AccountsApi
from restful_resources.categories import CategoriesApi


def initialize_routes(api):
    api.add_resource(AccountsApi, '/api/accounts')
    api.add_resource(CategoriesApi, '/api/categories')
