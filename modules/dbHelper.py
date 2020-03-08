import sqlite3
import json
from flask import jsonify
from modules.miscHelper import getDBPath


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def getAccounts(account='all', status='all'):
    db = sqlite3.connect(getDBPath())
    db.row_factory = dict_factory
    cursor = db.cursor()
    appendquery = statusquery = ""
    if account != "all":
        appendquery = "AND name = '%s'" % account
    if status != "all":
        statusquery = "AND status = '%s'" % status
    query = """
        SELECT name, balance, lastoperated, type, excludetotal, status
        FROM accounts
        WHERE 1 = 1 %s %s
        ORDER BY type
        """ % (appendquery, statusquery)
    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
    return jsonify(data)
