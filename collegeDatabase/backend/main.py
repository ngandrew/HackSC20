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
app = Flask(__name__)#, static_folder="static", static_url_path="")


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
    query = "SELECT * FROM colleges_data WHERE id IS NOT NULL "
    is_public = True if data.get("publicPrivate") == "public" else False if data.get("publicPrivate") == "private" else None
    if is_public != None:
        query += "AND is_public is {} ".format(is_public)
    if data.get("search"):
        query += "AND name LIKE '{}%'".format(data.get("search"))

    query += "LIMIT 50"
    res = []

    for row in [{column: value for column, value in rowproxy.items()} for rowproxy in db_session.execute(query)]:
        res.append({
            "id": row.get("id"),
            "name": row.get("name"),
            "city": row.get("city"),
            "state": row.get("state"),
            "publicPrivate": "public" if row.get("is_public") else "private",
            "sat_scores": row.get("sat_scores"),
            "act_scores": row.get("act_scores"),
            "expectedCost": get_average_price(row.get("cost_by_income"), int(data.get("income")) if data.get("income") else 50000),
            "difficulty": row.get("difficulty"),
            "calculatorLink": ("http://" if not row.get("price_calculator_url").startswith("http") else "") + row.get("price_calculator_url"),
            "deadline": row.get("r_admission"),
            "website": ("http://" if not row.get("school_url").startswith("http") else "") + row.get("school_url"),
        })

    return jsonify(res)

@app.route('/api/college_details')
def getCollegeDetails():
    id = int(request.values.get("id"))
    query = "SELECT * FROM colleges_data WHERE id = {}".format(id)
    row = {column: value for column, value in db_session.execute(query).fetchone().items()}
    if row:
        grad_within = row.get("grad_within")
        return jsonify({
            "name": row.get("name"),
            "city": row.get("city"),
            "state": row.get("state"),
            "publicPrivate": "public" if row.get("is_public") else "private",
            "sat_scores": row.get("sat_scores"),
            "act_scores": row.get("act_scores"),
            "expectedCost": get_average_price(row.get("cost_by_income"), 50000),
            "difficulty": row.get("difficulty"),
            "inState": row.get("in_state_tuition"),
            "outOfState": row.get("out_state_tuition"),
            "roomAndBoard": row.get("room_board"),
            "calculatorLink": ("http://" if not row.get("price_calculator_url").startswith("http") else "") + row.get("price_calculator_url"),
            "deadline": row.get("r_admission"),
            "website": ("http://" if not row.get("school_url").startswith("http") else "") + row.get("school_url"),
            "essays": row.get("essay"),
            "athletics": row.get("athletics_div"),
            "grad4": grad_within.get("4years_grate") if grad_within else None,
            "grad5": grad_within.get("5years_grate") if grad_within else None,
            "grad6": grad_within.get("6years_grate") if grad_within else None,
            "isUc": "University of California" in row.get("name"),
            "appFee": row.get("online_fee"),
            "classSize": row.get("ug_size"),
        })

    return jsonify({});


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
