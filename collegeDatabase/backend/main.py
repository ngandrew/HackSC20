import sys
sys.path.append(".")
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, String, MetaData
from sqlalchemy.orm import sessionmaker

from database import init_db
from database import db_session

from models import User, HelpText

init_db()
app = Flask(__name__)


@app.route('/helpData')
def helpData():
    query = db_session.query(HelpText).filter_by(page=request.values.get('location'))
    res = db_session.execute(query).fetchone()[2]
    return jsonify(res)

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response


@app.teardown_appcontext
def shutdown_session(exception=None):
    from database import db_session
    db_session.remove()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
