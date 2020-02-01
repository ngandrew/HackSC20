import sys
sys.path.append("/Users/ang/Documents/code/hack/HackSC20/collegeDatabase/backend")
from database import init_db
from database import db_session

from models import College

FN = "/Users/ang/Documents/code/hack/HackSC20/collegeDatabase/data/datasheet-full.csv"


init_db()

subCols = ["0-30000", "0-48000", "30001-48000", "48001-75000", "75001-110000", "110001-plus", "75000-plus", "30001-75000"]
netPriceKeys = {"public":{}, "private":{}}

with open(FN, "r", errors='replace') as f:
    f.readline()    # get rid of first one
    headers = f.readline().strip().split(',')
    f.readline()    # get rid of third one
    # types = f.readline().strip().split(',')
    header_list = []
    for i in range(len(headers)):
        # print(headers[i])
        if headers[i] == "id":
            idCol = i
        elif headers[i] == "name":
            nameCol = i
        elif headers[i] == "school_url":
            urlCol = i
        elif headers[i] == "price_calculator_url":
            pcUrlCol = i
        else:
            split = headers[i].split(".")
            if len(split)>1 and split[0] == "net_price":
                if split[len(split)-1] in subCols and split[1] in ["public", "private"]:
                    if not split[1] in netPriceKeys:
                        netPriceKeys[split[1]] = {}
                    netPriceKeys[split[1]][split[len(split)-1]] = i

    dataLine = f.readline()
    while dataLine:
        dataLine = dataLine.strip().split(',')
        print(db_session.query(College).get(dataLine[idCol]))
        if db_session.query(College).get(dataLine[idCol]) is not None:
            dataLine = f.readline()
            continue
        is_public = dataLine[netPriceKeys["public"][subCols[0]]] != "NULL" and dataLine[netPriceKeys["public"][subCols[1]]] != "NULL"
        pubstr = "public" if is_public else "private"
        listnetprices = {}
        for postfix in subCols:
            listnetprices[postfix] = dataLine[netPriceKeys[pubstr][postfix]]
        netpriceints = {k: int(v) for k,v in listnetprices.items() if v != "NULL"}
        college = College(id=dataLine[idCol], is_public=is_public,name=dataLine[nameCol],cost_by_income=netpriceints,price_calculator_url=dataLine[pcUrlCol],school_url=dataLine[urlCol])
        db_session.add(college)
        db_session.commit()

        dataLine = f.readline()


    # line = f.readline().strip()
    # while line != "":
    #     col = College(line, header_list)
    #     db_session.add(col)
    #     db_session.commit()
    #     line = f.readline().strip()


