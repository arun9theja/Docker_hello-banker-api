import os
from flask import current_app as app


def getDBPath():
    return os.path.join(app.config['SQLITE_DB_DIR'],
                        app.config['SQLITE_DB_FILE'])