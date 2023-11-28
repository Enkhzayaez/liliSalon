import json
import psycopg2

def connect():
    con = psycopg2.connect(
        dbname = 'Salon',
        user = 'postgres',
        password = 'z02212205',
        host = 'localhost',
        port = '5432',
    )
    return con

def sendResponse(resultCode , resultMessege, data, action):
    resp = {}
    resp["resultCode"] = resultCode
    resp["resultMessege"] = resultMessege
    resp["data"] = data
    resp["size"] = len(data)
    resp["action"] = action
    return json.dumps(resp)