from flask_restful import Resource
from modules.dbHelper import getAccounts


class AccountsApi(Resource):
    def get(self):
        return getAccounts()
