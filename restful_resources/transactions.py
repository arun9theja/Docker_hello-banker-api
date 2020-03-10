from flask import request
from flask_restful import Resource
from modules.dbHelper import getTransactions
        

class TransactionsListApi(Resource):
    def get(self):
        account = request.args.get("account", default=None)
        period  = request.args.get("period", default=None)
        year    = request.args.get("year", default=None)
        month   = request.args.get("month", default=None)
        return getTransactions(account, period, year, month)