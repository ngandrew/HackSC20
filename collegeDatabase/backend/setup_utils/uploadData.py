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
        elif headers[i] == "act_scores.midpoint.cumulative":
            actCol = i
        elif headers[i] == "sat_scores.average.overall":
            satCol = i
        elif headers[i] == "size":
            szCol = i
        elif headers[i] == "carnegie_size_setting":
            szCodeCol = i   # used to see if only post-grad
        elif headers[i] == "completion_rate_4yr_150nt":
            cmplRate1Col = i
        elif headers[i] == "completion_rate_less_than_4yr_150nt":
            cmplRate2Col = i
        elif headers[i] == "city":
            cityCol = i
        elif headers[i] == "state":
            stateCol = i
        else:
            split = headers[i].split(".")
            if len(split)>1 and split[0] == "net_price":
                if split[len(split)-1] in subCols and split[1] in ["public", "private"]:
                    if not split[1] in netPriceKeys:
                        netPriceKeys[split[1]] = {}
                    netPriceKeys[split[1]][split[len(split)-1]] = i

    dl = f.readline()
    while dl:
        dl = dl.strip().split(',')
        # print(db_session.query(College).get(dl[idCol]))
        if db_session.query(College).get(dl[idCol]) is not None:
            dl = f.readline()
            continue
        is_public = dl[netPriceKeys["public"][subCols[0]]] != "NULL" and dl[netPriceKeys["public"][subCols[1]]] != "NULL"
        pubstr = "public" if is_public else "private"
        listnetprices = {}
        for postfix in subCols:
            listnetprices[postfix] = dl[netPriceKeys[pubstr][postfix]]
        netpriceints = {k: int(v) for k,v in listnetprices.items() if v != "NULL"}

        cmplRt = dl[cmplRate1Col] if dl[cmplRate1Col] != "NULL"  else dl[cmplRate2Col]
        if cmplRt == "NULL":
            cmplRt = None
        med_sat = dl[satCol] if dl[satCol] != "NULL" else None
        med_act = dl[actCol] if dl[actCol] != "NULL" else None

        if netpriceints != {} and db_session.query(College).get(dl[idCol]) is None and int(dl[szCol]) > 0 and dl[szCodeCol] != 18:
            college = College(id=dl[idCol], is_public=is_public,name=dl[nameCol],cost_by_income=netpriceints,price_calculator_url=dl[pcUrlCol],school_url=dl[urlCol], med_sat=med_sat,med_act=med_act,ug_size=dl[szCol], cmpl_rt_150=cmplRt,state=dl[stateCol], city=dl[cityCol])
            db_session.add(college)
            db_session.commit()

        dl = f.readline()


    # line = f.readline().strip()
    # while line != "":
    #     col = College(line, header_list)
    #     db_session.add(col)
    #     db_session.commit()
    #     line = f.readline().strip()


