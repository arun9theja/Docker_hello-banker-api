from flask_restful import Resource
from modules.dbHelper import getAccounts, getAccountNames


class AccountApi(Resource):
    def get(self):
        return getAccountNames()


class AccountsDetailApi(Resource):
    def get(self):
        return getAccounts()

if __name__ == "__main__":
    pass
