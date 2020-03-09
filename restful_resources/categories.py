from flask import request
from flask_restful import Resource
from modules.dbHelper import getCategories
        

class CategoriesApi(Resource):
    def get(self):
        type = request.args.get("type", default="all")
        return getCategories(type)