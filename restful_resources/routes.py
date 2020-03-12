from restful_resources.account import AccountsApi, DistinctAccountTypesApi
from restful_resources.categories import CategoriesApi
from restful_resources.transactions import TransactionsListApi, AddTransactionApi


def initialize_routes(api):
    api.add_resource(AccountsApi, '/api/accounts')
    api.add_resource(CategoriesApi, '/api/categories')
    api.add_resource(DistinctAccountTypesApi, '/api/distinctaccounts')
    api.add_resource(TransactionsListApi, '/api/listtransactions')
    api.add_resource(AddTransactionApi, '/api/addtransaction')
