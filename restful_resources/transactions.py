from flask import request
from flask_restful import Resource
from modules.dbHelper import getTransactions, addTransactionsDB
        

class TransactionsListApi(Resource):
    def get(self):
        account = request.args.get("account", default=None)
        period  = request.args.get("period", default=None)
        year    = request.args.get("year", default=None)
        month   = request.args.get("month", default=None)
        return getTransactions(account, period, year, month)

class AddTransactionApi(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        account = json_data["account"]
        category = json_data["category"]
        amount = json_data["amount"]
        date = json_data["date"]
        notes = json_data["notes"]
        return addTransactionsDB(date, notes, amount, category, account)
