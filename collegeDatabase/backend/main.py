import sys
sys.path.append(".")
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, String, MetaData
from sqlalchemy.orm import sessionmaker
import json

from database import init_db
from database import db_session

from models import HelpText, College

init_db()
app = Flask(__name__, static_folder="static", static_url_path="")


@app.route('/api/helpData')
def helpData():
    query = db_session.query(HelpText).filter_by(page=request.values.get("location"))
    res = db_session.execute(query).fetchone()[2]
    return jsonify(res)

def get_average_price(cost_by_income, income):
    if cost_by_income == {}:
        return False

    MAX_VAL = 999999999
    min_range = MAX_VAL
    price = 0
    for k, v in cost_by_income.items():
        lohi = k.split("-")
        lo = int(lohi[0])
        is_plus = lohi[1] == "plus"
        if is_plus:
            hi = MAX_VAL
        else:
            hi = int(lohi[1])
        if lo <= income and (is_plus or income <= hi) and hi - lo < min_range:
            price = v
    return price

@app.route('/api/colleges')
def searchColleges():
    data = json.loads(request.values.get("data"))
    query = "SELECT * FROM colleges WHERE id IS NOT NULL "
    is_public = True if request.values.get("publicPrivate") == "public" else False if data.get("publicPrivate") == "private" else None
    if is_public != None:
        query += "AND is_public is {} ".format(is_public)

    query += "LIMIT 50"
    res = []

    for row in [{column: value for column, value in rowproxy.items()} for rowproxy in db_session.execute(query)]:
        res.append({
            "id": row["id"],
            "name": row["name"],
            "city": "Los Angeles",
            "state": "CA",
            "publicPrivate": "public" if row["is_public"] else "private",
            "sat25": 800,
            "sat75": 1500,
            "act25": 28,
            "act75": 35,
            "expectedCost": get_average_price(row["cost_by_income"], int(data.get("income")) if data.get("income") else 50000),
            "difficulty": "very difficult",
            "calculatorLink": ("http://" if not row["price_calculator_url"].startswith("http") else "") + row["price_calculator_url"],
            "deadline": "1/23",
            "website": ("http://" if not row["school_url"].startswith("http") else "") + row["school_url"],
        })

    return jsonify(res)


@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def index(path):
    return app.send_static_file(path)

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
