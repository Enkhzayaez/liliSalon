from django.http import HttpResponse
from django.shortcuts import render
import json
import psycopg2
from django.views.decorators.csrf import csrf_exempt

def sendResponse(resultCode , resultMessege, data, action):
    resp = {}
    resp["resultCode"] = resultCode
    resp["resultMessege"] = resultMessege
    resp["data"] = data
    resp["size"] = len(data)
    resp["action"] = action
    return json.dumps(resp)

def connect():
    con = psycopg2.connect(
        dbname = 'Salon',
        user = 'postgres',
        password = 'z02212205',
        host = 'localhost',
        port = '5432',
    )
    return con

@csrf_exempt
def login(request):
    jsond = json.loads(request.body)
    action = jsond.get('action', 'nokey')
    phone = jsond.get('phone', 'nokey')
    password = jsond.get('password', 'nokey')
    con = connect()
    cursor = con.cursor()
    cursor.execute(f"""SELECT id, username, phone, email FROM t_user WHERE phone = '{phone}' AND password = '{password}' """)
    columns = cursor.description
    respRow = [{columns[index][0]:column for index,
                column in enumerate(value)} for value in cursor.fetchall()]
    if len(respRow) == 1:
        print('zar zasagdsan')
        resp = sendResponse(200, 'success', respRow ,  action)
        return HttpResponse(resp)
    else:
        resp = sendResponse(400, 'error', "" ,action)
        return HttpResponse(resp)
    
@csrf_exempt
def register(request):
    jsond = json.loads(request.body)
    action = jsond.get('action', 'nokey')
    phone = jsond.get('phone', 'nokey')
    password = jsond.get('password', 'nokey')
    username = jsond.get('username', 'nokey')
    email = jsond.get('email', 'nokey')
    con = connect()
    cursor = con.cursor()
    cursor.execute(f"""SELECT * FROM t_user WHERE phone = '{phone}' AND password = '{password}' """)
    temp_checker = cursor.fetchall()
   
    if not temp_checker:
        cursor.execute(f"""INSERT INTO public.t_user(username, phone, email, password)
                        VALUES ('{username}', '{phone}', '{email}', '{password}');""")
        con.commit()
        resp = sendResponse(200, 'success', "" ,action)
        return HttpResponse(resp)
    else:
        resp = sendResponse(404, 'There is user with credentials', "" ,action)
        return HttpResponse(resp)

@csrf_exempt
def admin(request):
    return HttpResponse() 

def main(request):
    jsond = json.loads(request.body)
    action = jsond.get('action', 'nokey')
    resp = "Working not fine"
    if action == "add_category":
        resp = add_category(request)
    if action == "add_sub_category":
        resp = add_sub_category(request)
    if action == "Bye":
        resp = "Good bye"
    return HttpResponse(resp)

def add_category(request):
    jsond = json.loads(request.body)
    name = jsond.get("name")
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(f'''SELECT * FROM t_category WHERE name = '{name}';''')
        cat = cur.fetchall()
        if cat == []:
            resp = sendResponse(402, 'already category with same name', "" ,action)
        else:
            cur.execute(f''' INSERT INTO t_category(
                            id, name)
                            VALUES (DEFAULT,'{name}');''')
            con.commit()
            resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, 'error', "" ,action)
    return resp

def add_sub_category(request):
    jsond = json.loads(request.body)
    name = jsond.get("name")
    cat_id = jsond.get("cat_id")
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(f'''SELECT * FROM t_sub_category WHERE name = '{name}';''')
        cat = cur.fetchall()
        if cat  != []:
            resp = sendResponse(402, 'already sub category with same name', "" ,action)
        else:
            cur.execute(f''' INSERT INTO t_sub_category(
                            id, category_id, name)
                            VALUES (DEFAULT,{cat_id},'{name}');''')
            con.commit()
            resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, 'error', e ,action)
    return resp

def add_branch(request):
    jsond = json.loads(request.body)
    name = jsond.get("name")
    cat_id = jsond.get("cat_id")
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(f'''SELECT * FROM t_sub_category WHERE name = '{name}';''')
        cat = cur.fetchall()
        if cat  != []:
            resp = sendResponse(402, 'already sub category with same name', "" ,action)
        else:
            cur.execute(f''' INSERT INTO t_sub_category(
                            id, category_id, name)
                            VALUES (DEFAULT,{cat_id},'{name}');''')
            con.commit()
            resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, 'error', e ,action)
    return resp




















# def getAngilal(request):
#     action = 'getAngilal'
#     con = connect()
#     cursor = con.cursor()
#     cursor.execute("SELECT * FROM public.t_angilal;")
#     columns = cursor.description
#     respRow = [{columns[index][0]:column for index,
#                 column in enumerate(value)} for value in cursor.fetchall()]
#     resp = sendResponse('200', "success", respRow, action)
#     return HttpResponse(resp)


# def insertZar(request):
    print("zarnemegdeh gej bna")
    action = 'insertZar'
    # print(request.body)
    jsond = json.loads(request.body)
    action = jsond.get('action', 'nokey')
    title = jsond.get('title', 'nokey')
    charter = str(jsond.get('charter', 'nokey'))
    address = str(jsond.get('address', 'nokey'))
    tsalin = jsond.get('tsalin', 'nokey')
    aid = jsond.get('aid', 'nokey')
    uid = jsond.get('uid', 'nokey')

    con = connect()
    cursor = con.cursor()
    cursor.execute(f"""INSERT INTO public.t_zar( z_title, z_charter, z_address, z_tsalin, a_id, u_id)
	                                VALUES ('{title}', '{charter}', '{address}', '{tsalin}', '{aid}', '{uid}');""")
    con.commit()
    print('zar nemegdsen')
    resp = sendResponse('200', 'success', '',  action)

    return HttpResponse(resp)


