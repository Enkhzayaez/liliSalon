from django.http import HttpResponse
import json
import hashlib
from django.views.decorators.csrf import csrf_exempt
from server.utils import *

def list_operator(request):
    jsond = json.loads(request.body)
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(f'''SELECT * FROM t_operator;''')
        columns = cur.description
        respRow = [{columns[index][0]:column for index,
                    column in enumerate(value)} for value in cur.fetchall()]
        resp = sendResponse(200, 'success', respRow ,  action)
    except Exception as e:
        resp = sendResponse(401, 'error', "" ,action)
    return resp



def add_operator(request):
    jsond = json.loads(request.body)
    lastname = jsond.get("lastname")
    firstname = jsond.get("firstname")
    phone = jsond.get("phone")
    email = jsond.get("email")
    branch_id = jsond.get("branch_id")
    admin_id = jsond.get("admin_id")
    password = jsond.get("password")
    action = jsond.get("action")
    password = mandakhHash(password)
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(f'''SELECT * FROM t_operator WHERE email = '{email}' OR phone = '{phone}';''')
        cat = cur.fetchall()
        if cat != []:
            resp = sendResponse(402, 'already operator with same email or phone', "" ,action)
        else:
            print(f'''INSERT INTO t_operator(
                            id, lastname, firstname, phone, email, password, regdate, admin_id, branch_id)
                            VALUES (DEFAULT, {lastname}, {firstname}, {phone}, {email}, {password}, NOW(), {admin_id}, {branch_id});''')
            cur.execute('''INSERT INTO t_operator(
                            id, lastname, firstname, phone, email, password, regdate, admin_id, branch_id)
                            VALUES (DEFAULT, %s, %s, %s, %s, %s, NOW(), %s, %s);''',[lastname,firstname,phone,email,password,admin_id,branch_id])
            con.commit()
            resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, 'error', "" ,action)
    return resp


@csrf_exempt
def main(request):
    jsond = json.loads(request.body)
    action = jsond.get('action')
    resp = sendResponse(401, 'working not fine', "" ,action)
    if action == "add_operator":
        resp = add_operator(request)
    if action == "list_operator":
        resp = list_operator(request)    
    return HttpResponse(resp)