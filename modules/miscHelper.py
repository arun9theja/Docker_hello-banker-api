import os
from flask import current_app as app
from flask import jsonify


def getDBPath():
    return os.path.join(app.config['SQLITE_DB_DIR'],
                        app.config['SQLITE_DB_FILE'])


def categoryStats(category):
    from modules.dbHelper import getCategoryStats
    year_month_data = getCategoryStats(category, period="YEAR_MONTH")
    year_data = getCategoryStats(category, period="YEAR")
    finalStats = [{"year_month_data": year_month_data}, {"year_data": year_data}]
    return jsonify(finalStats)
