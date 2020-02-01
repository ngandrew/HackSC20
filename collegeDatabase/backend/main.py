import sys
sys.path.append(".")
from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, String, MetaData
from sqlalchemy.orm import sessionmaker

from database import init_db
from database import db_session

from models import User

init_db()
app = Flask(__name__)


@app.route('/helpData')
def helpData():
    res = {}
    res["data"] = [
        {
            "id": 'student_firstName',
            "description": 'It\'s your name :/',
        },
        {
            "id": 'student_middleInit',
            "description": 'middle initial pls (optional)',
        },
        {
            "id": 'student_lastName',
            "description": 'ur last name',
        },
        {
            "id": 'student_dob',
            "description": 'when u were born',
            "link": 'https://www.shutterfly.com/ideas/wp-content/uploads/2016/08/50-happy-birthday-quotes-thumb.jpg'
        }
    ]
    return jsonify(res)
    # u = User(name="Bob", email="a@b.com")
    # db_session.add(u)
    # db_session.commit()
    # if os.environ.get('GAE_ENV') == 'standard':
    #     # If deployed, use the local socket interface for accessing Cloud SQL
    #     host = '/cloudsql/{}'.format(db_connection_name)
    # else:
    #     # If running locally, use the TCP connections instead
    #     # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
    #     # so that your application can use 127.0.0.1:3306 to connect to your
    #     # Cloud SQL instance
    #     host = '127.0.0.1'


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
