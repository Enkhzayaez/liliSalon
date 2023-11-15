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
    print(respRow)
    print("Hello")
    print(phone)
    print(password)
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


def admin(request):
    return HttpResponse() 





















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


