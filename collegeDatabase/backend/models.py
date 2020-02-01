from sqlalchemy import Column, Integer, String, Boolean
# from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import JSON
from database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)


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


    def __init__(self, id=None, is_public=None,name=None, cost_by_income=None, price_calculator_url=None, school_url=None):
        self.id = id
        self.name = name
        self.is_public = is_public
        self.cost_by_income = cost_by_income
        self.price_calculator_url = price_calculator_url
        self.school_url = school_url


    # def get_average_price(self, income):
    #     MAX_VAL = 999999
    #     min_rane = MAX_VAL
    #     for k, v in self.cost_by_income:
    #         lohi = k.split("-")
    #         lo =


