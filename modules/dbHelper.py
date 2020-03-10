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

def getCategories(type='all'):
    db = sqlite3.connect(getDBPath())
    db.row_factory = dict_factory
    cursor = db.cursor()
    condquery = ""
    if not type == "all":
        condquery = "AND type = '%s'" % type
    query = """
        SELECT name, type FROM categories
        WHERE 1 = 1 %s
        ORDER BY type
        """ % condquery
    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
    return jsonify(data)

def getDistinctAccountTypes():
    db = sqlite3.connect(getDBPath())
    db.row_factory = dict_factory
    cursor = db.cursor()
    query = """
        SELECT DISTINCT(type) as name
        FROM accounts
        ORDER BY name
        """
    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
    return jsonify(data)

def getTransactions(accountname, period=None, year=None, month=None):
    db = sqlite3.connect(getDBPath())
    db.row_factory = dict_factory
    cursor = db.cursor()

    advQuery = limitQuery = ''

    if period is None:
        limitQuery = 'LIMIT 50'
    else:
        if 'PRE_' in period:
            if 'thisweek' in period:
                advQuery = "AND STRFTIME('%Y%W', opdate) = STRFTIME('%Y%W', DATE('NOW'))"
            elif 'thismonth' in period:
                advQuery = "AND opdate >= DATE('NOW', 'START OF MONTH')"
            elif 'lastmonth' in period:
                advQuery = "AND opdate BETWEEN DATE('NOW', 'START OF MONTH', '-1 MONTH') AND DATE('NOW', 'START OF MONTH')"
        elif 'selective' in period:
            advQuery = "AND STRFTIME('%Y', opdate) = '{0}' AND STRFTIME('%m', opdate) = '{1}'".format(
                year, month)

    query = "SELECT opdate, description, credit, debit, category \
            FROM transactions \
            WHERE account = '%s' %s \
            ORDER BY opdate DESC %s" \
            % (accountname, advQuery, limitQuery)

    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
    return jsonify(data)