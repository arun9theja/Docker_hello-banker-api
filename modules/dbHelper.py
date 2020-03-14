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


def fundTransferDB(date, notes, amount, fromAccount, toAccount):
    addTransactionsDB(date, notes, amount, "TRANSFER OUT", fromAccount)
    addTransactionsDB(date, notes, amount, "TRANSFER IN", toAccount)
    return jsonify({"status": "Funds Transfered successfully"})


def addTransactionsDB(date, notes, amount, category, account):
    db = sqlite3.connect(getDBPath())
    cursor = db.cursor()

    credit, debit, updatetype = ["NULL", amount, "debit"]
    if getCategoryType(category) == "IN":
        credit, debit, updatetype = [amount, "NULL", "credit"]

    query = """
        INSERT INTO transactions 
        VALUES('%s', '%s', '%s', %s, %s, '%s')""" % (date, notes, category,
                                                     credit, debit, account)
    cursor.execute(query)
    data = cursor.fetchall()
    db.commit()
    db.close()
    if len(data) == 0:
        if updateAccounts(account, amount, updatetype):
            returnString = {"status": "Transaction added successfully"}
        else:
            returnString = {
                "status":
                "Failed to update accounts table. But transaction recorded"
            }
    else:
        returnString = {"status": str(data[0])}

    return jsonify(returnString)


def getCategoryType(category):
    db = sqlite3.connect(getDBPath())
    cursor = db.cursor()

    query = "SELECT type FROM categories WHERE name = '%s'" % category
    cursor.execute(query)
    data = cursor.fetchone()
    db.close()
    return data[0]


def updateAccounts(name, amount, updatetype):
    db = sqlite3.connect(getDBPath())
    cursor = db.cursor()

    sign, operator = ["+", "-"]
    isassetAcc = checkAccountType(name)
    if not isassetAcc:
        sign = "-"
    if updatetype == "credit":
        operator = "+"

    query = """UPDATE accounts
            SET balance = balance %s %s%s, lastoperated = DATE('NOW')
            WHERE name = '%s'""" % (operator, sign, amount, name)
    cursor.execute(query)
    db.commit()
    db.close()
    return True


def checkAccountType(account):
    db = sqlite3.connect(getDBPath())
    cursor = db.cursor()
    isassetAcc = True

    query = "SELECT type FROM accounts WHERE name = '%s'" % account
    cursor.execute(query)
    data = cursor.fetchone()

    db.close()

    if data[0] == "Credit Card":
        isassetAcc = False
    return isassetAcc


def getMonthStats(month=None):
    db = sqlite3.connect(getDBPath())
    db.row_factory = dict_factory
    cursor = db.cursor()

    advQuery = "AND opdate >= DATE('NOW', 'START OF MONTH')"

    if not month is None:
        advQuery = "AND opdate BETWEEN DATE('NOW', 'START OF MONTH', '-1 MONTH') AND DATE('NOW', 'START OF MONTH')"

    query = """
        SELECT category, SUM(debit) AS debit, SUM(credit) AS credit
        FROM transactions
        WHERE category NOT IN ('TRANSFER IN', 'TRANSFER OUT') %s
        GROUP BY category
        ORDER BY debit DESC, credit DESC
        """ % advQuery

    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
    return jsonify(data)


def getDescriptionSuggestions(keyword, type="regular", limit=10):
    db = sqlite3.connect(getDBPath())
    db.row_factory = dict_factory
    cursor = db.cursor()

    query = """
        SELECT DISTINCT(description) AS description 
        FROM transactions 
        WHERE description LIKE '%%%s%%'
        ORDER BY opdate DESC LIMIT %d
        """ % (keyword, limit)
    
    if not "regular" in type:
        query = """
            SELECT DISTINCT(description) AS description 
            FROM transactions 
            WHERE description LIKE '%%%s%%'
                AND category IN ('TRANSFER IN', 'TRANSFER OUT')
            ORDER BY opdate DESC LIMIT %d
            """ % (keyword, limit)

    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
    return jsonify(data)
