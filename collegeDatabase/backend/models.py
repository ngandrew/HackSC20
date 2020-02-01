from sqlalchemy import Column, Integer, String, Boolean,  Float
# from sqlalchemy.dialects.postgresql import ARRAY
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

    med_act = Column(Float)
    med_sat = Column(Float)

    ug_size = Column(Integer)
    cmpl_rt_150 = Column(Float)

    def __init__(self, id=None, is_public=None, name=None, cost_by_income=None, price_calculator_url=None, school_url=None, med_act=None, med_sat=None, ug_size=None, cmpl_rt_150=None, city=None, state=None):
        self.id = id
        self.name = name
        self.is_public = is_public
        self.cost_by_income = cost_by_income
        self.price_calculator_url = price_calculator_url
        self.school_url = school_url
        self.med_sat = med_sat
        self.med_act = med_act
        self.ug_size = ug_size
        self.cmpl_rt_150 = cmpl_rt_150
        self.city = city
        self.state = state

    def get_average_price(self, income):
        if self.cost_by_income == {}:
            return False

        MAX_VAL = 999999999
        min_range = MAX_VAL
        for k, v in self.cost_by_income:
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
