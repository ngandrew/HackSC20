import sys
sys.path.append("/Users/ang/Documents/code/hack/HackSC20/collegeDatabase/backend")
from database import init_db
from database import db_session

# from models import User

FN = "/Users/ang/Documents/code/hack/HackSC20/collegeDatabase/data/datasheet-full.csv"


init_db()


class College(Base):
    __tablename__ = 'colleges'

    def __init__(self, line, header_list):
        fields = line.split(',')
        for i in range(fields):
            header_name, header_type = header_list[i]
            parsed = fields[i].rsplit('.', 1)
            if len(parsed) == 2:
                nextheader_name, nextheader_type = header_list[i+1]
                while (nextheader_name.rsplit('.',1)[0] = parsed)
                    i++



    # id = Column(Integer, primary_key=True)
    # name = Column(String(100), unique=True)
    # cost_by_income = Column(ARRAY(Integer))


with open(FN, "r") as f:
    f.readline()    # get rid of first one
    header_line = f.readline().strip()
    headers = header_line.split(',')
    types = f.readline().strip().split(',')
    header_list = []
    for i in range(headers):
        header_list[i] = (headers[i], types[i])
    f.readline()    # get rid of third one
    size = len(headers)

    line = f.readline().strip()
    while line != "":
        col = College(line, header_list)
        db_session.add(col)
        db_session.commit()
        line = f.readline().strip()


