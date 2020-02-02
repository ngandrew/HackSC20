from sqlalchemy import Column, Integer, String, Boolean,  Float
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import JSON
from database import Base


# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50), unique=True)
#     email = Column(String(120), unique=True)

#     def __init__(self, name=None, email=None):
#         self.name = name
#         self.email = email

#     def __repr__(self):
#         return '<User %r>' % (self.name)


class HelpText(Base):
    __tablename__ = 'help_text'
    id = Column(Integer, primary_key=True)
    page = Column(String(350))
    helpData = Column(JSON)

    def __init__(self, id=None, page=None, helpData=None):
        self.id = id
        self.page = page
        self.helpData = helpData


class NewCollege(Base):
    __tablename__ = 'colleges_data'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    # cost_by_income = Column(ARRAY(Integer))
    cost_by_income = Column(JSON)
    is_public = Column(Boolean)
    school_url = Column(String(200))
    price_calculator_url = Column(String(200))

    city = Column(String(30))
    state = Column(String(5))

    # med_act = Column(Float)
    # med_sat = Column(Float)
    act_scores = Column(ARRAY(Float))
    sat_scores = Column(ARRAY(Float))

    ug_size = Column(Integer)
    cmpl_rt_150 = Column(Float)

    r_admission = Column(String(30))
    online_fee = Column(Integer)
    essay = Column(Boolean)
    grad_within = Column(JSON)
    difficulty = Column(String(100))
    med_gpa = Column(Float)
    room_board = Column(Integer)
    athletics_div = Column(String(100))

    in_state_tuition = Column(Integer)
    out_state_tuition = Column(Integer)

    # {"name": "Alaska Pacific University", "r_admission": "Rolling", "online_fee": 50, "essay": false, "grad_within": {"4years_grate": 36.4, "5years_grate": null, "6years_grate": null}, "website": "http://www.alaskapacific.edu", "difficulty": "Minimally difficult", "gpa": 3.22, "room_board": 8230, "athletics_div": "\u00a0"}



    def __init__(self, id=None, is_public=None, name=None, cost_by_income=None, price_calculator_url=None, school_url=None, sat_scores=None, act_scores=None, ug_size=None, cmpl_rt_150=None, city=None, state=None, r_admission=None, online_fee=None, essay=None, grad_within=None, difficulty = None, med_gpa=None, room_board=None, athletics_div=None, in_state_tuition=None, out_state_tuition=None):
        self.id = id
        self.name = name
        self.is_public = is_public
        self.cost_by_income = cost_by_income
        self.price_calculator_url = price_calculator_url
        self.school_url = school_url
        self.act_scores = act_scores
        self.sat_scores = sat_scores
        self.ug_size = ug_size
        self.cmpl_rt_150 = cmpl_rt_150
        self.city = city
        self.state = state
        self.r_admission = r_admission
        self.online_fee = online_fee
        self.essay = essay
        self.grad_within = grad_within
        self.difficulty = difficulty
        self.med_gpa = med_gpa
        self.room_board = room_board
        self.athletics_div = athletics_div
        self.in_state_tuition = in_state_tuition
        self.out_state_tuition = out_state_tuition


class College(Base):
    __tablename__ = 'colleges'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    # cost_by_income = Column(ARRAY(Integer))
    cost_by_income = Column(JSON)
    is_public = Column(Boolean)
    school_url = Column(String(200))
    price_calculator_url = Column(String(200))

    city = Column(String(30))
    state = Column(String(5))

    act_scores = Column(ARRAY(Float))
    sat_scores = Column(ARRAY(Float))

    ug_size = Column(Integer)
    cmpl_rt_150 = Column(Float)

    in_state_tuition = Column(Integer)
    out_state_tuition = Column(Integer)

    def __init__(self, id=None, is_public=None, name=None, cost_by_income=None, price_calculator_url=None, school_url=None, act_scores=None, sat_scores=None, ug_size=None, cmpl_rt_150=None, city=None, state=None, in_state_tuition=None, out_state_tuition=None):
        self.id = id
        self.name = name
        self.is_public = is_public
        self.cost_by_income = cost_by_income
        self.price_calculator_url = price_calculator_url
        self.school_url = school_url
        self.act_scores = act_scores
        self.sat_scores = sat_scores
        self.ug_size = ug_size
        self.cmpl_rt_150 = cmpl_rt_150
        self.city = city
        self.state = state
        self.in_state_tuition = in_state_tuition
        self.out_state_tuition = out_state_tuition
