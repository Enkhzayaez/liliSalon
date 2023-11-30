import json
import psycopg2
import hashlib
import bson

def connect():
    con = psycopg2.connect(
        dbname = 'postgres',
        user = 'postgres',
        password = '153298',
        host = 'localhost',
        port = '5433',
    )
    return con

def mandakhHash(password):
    return hashlib.md5(password.encode('utf-8')).hexdigest()

def sendResponse(resultCode , resultMessege, data, action):
    resp = {}
    resp["resultCode"] = resultCode
    resp["resultMessege"] = resultMessege
    resp["data"] = data
    resp["action"] = action
    return json.dumps(resp, indent=4, sort_keys=True, default=str)