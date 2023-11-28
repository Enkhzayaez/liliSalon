from django.http import HttpResponse
import json
import hashlib
from django.views.decorators.csrf import csrf_exempt
from server.utils import *

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

def add_category(request):
    jsond = json.loads(request.body)
    name = jsond.get("name")
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(f'''SELECT * FROM t_category WHERE name = '{name}';''')
        cat = cur.fetchall()
        if cat != []:
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
    address = jsond.get("address")
    operator_id = jsond.get("operator_id")
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(f'''SELECT * FROM t_branch WHERE address = '{address}';''')
        cat = cur.fetchall()
        if cat  != []:
            resp = sendResponse(402, 'already branch with same address', "" ,action)
        else:
            cur.execute(f'''INSERT INTO t_branch(
                            id, address, operator_id, image)
                            VALUES (DEFAULT, {address}, {operator_id}, 'Nothing');''')
            con.commit()
            resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, 'error', e ,action)
    return resp

def list_category(request):
    jsons = json.loads(request.body)
    action = jsons.get('action')
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(f'''SELECT * FROM t_category;''')
        columns = cur.description
        respRow = [{columns[index][0]:column for index,
                    column in enumerate(value)} for value in cur.fetchall()]
        resp = sendResponse(200, 'success', respRow ,  action)
    except Exception as e:
        resp = sendResponse(401, 'error', e ,action)
    return resp

def list_sub_category(request):
    jsons = json.loads(request.body)
    action = jsons.get('action')
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(f'''SELECT * FROM t_sub_category;''')
        columns = cur.description
        respRow = [{columns[index][0]:column for index,
                    column in enumerate(value)} for value in cur.fetchall()]
        resp = sendResponse(200, 'success', respRow ,  action)
    except Exception as e:
        resp = sendResponse(401, 'error', e ,action)
    return resp

def list_branch(request):
    jsons = json.loads(request.body)
    action = jsons.get('action')
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(f'''SELECT * FROM t_branch;''')
        columns = cur.description
        respRow = [{columns[index][0]:column for index,
                    column in enumerate(value)} for value in cur.fetchall()]
        resp = sendResponse(200, 'success', respRow ,  action)
    except Exception as e:
        resp = sendResponse(401, 'error', e ,action)
    return resp

def edit_category(request):
    jsond = json.loads(request.body)
    name = jsond.get("name")
    cat_id = jsond.get("cat_id")
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(f'''SELECT * FROM t_category WHERE id = '{cat_id}';''')
        cat = cur.fetchall()
        if cat == []:
            resp = sendResponse(402, 'no category found', "" ,action)
        else:
            cur.execute(f'''UPDATE t_category
                            SET name='{name}' 
                            WHERE id = '{cat_id}';''')
            con.commit()
            resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, 'error', e ,action)
    return resp

def edit_branch(request):
    jsond = json.loads(request.body)
    address = jsond.get("address")
    operator_id = jsond.get("operator_id")

    id = jsond.get("id")
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(f'''SELECT * FROM t_branch WHERE id = '{id}';''')
        cat = cur.fetchall()
        if cat == []:
            resp = sendResponse(402, 'no branch found', "" ,action)
        else:
            cur.execute(f'''UPDATE t_branch
                            SET address=?, operator_id=?,
                            WHERE id = {id};''')
            con.commit()
            resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, 'error', e ,action)
    return resp

def edit_sub_category(request):
    jsond = json.loads(request.body)
    name = jsond.get("name")
    sub_id = jsond.get("sub_id")
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(f'''SELECT * FROM t_sub_category WHERE id = '{sub_id}';''')
        cat = cur.fetchall()
        if cat == []:
            resp = sendResponse(402, 'no category found', "" ,action)
        else:
            cur.execute(f'''UPDATE t_sub_category
                            SET name='{name}' 
                            WHERE id = '{sub_id}';''')
            con.commit()
            resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, 'error', e ,action)
    return resp

def delete_sub_category(request):
    jsond = json.loads(request.body)
    sub_id = jsond.get("sub_id")
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(f'''SELECT * FROM t_sub_category WHERE id = '{sub_id}';''')
        cat = cur.fetchall()
        if cat == []:
            resp = sendResponse(402, 'no category found', "" ,action)
        else:
            cur.execute(f'''DELETE FROM t_sub_category
	                        WHERE id = {sub_id};''')
            con.commit()
            resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, 'error', e ,action)
    return resp

def delete_category(request):
    jsond = json.loads(request.body)
    cat_id = jsond.get("cat_id")
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(f'''SELECT * FROM t_category WHERE id = '{cat_id}';''')
        cat = cur.fetchall()
        if cat == []:
            resp = sendResponse(402, 'no category found', "" ,action)
        else:
            cur.execute(f'''DELETE FROM t_category
	                        WHERE id = {cat_id};''')
            con.commit()
            resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, 'error', e ,action)
    return resp






def add_operator(request):
    jsond = json.loads(request.body)
    lastname = jsond.get("lastname")
    firstname = jsond.get("firstname")
    phone = jsond.get("phone")
    email = jsond.get("email")
    branch_id = jsond.get("branch_id")
    password = jsond.get("password")
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:

        cur.execute(f'''SELECT * FROM t_operator WHERE email = '{email}' OR phone = '{phone}';''')
        cat = cur.fetchall()
        if cat != []:
            resp = sendResponse(402, 'already operator with same email or phone', "" ,action)
        else:
            cur.execute(f'''INSERT INTO t_operator(
	                        id, lastname, firstname, phone, email, branch_id, reg_date, is_active, password)
	                        VALUES (DEFAULT, {lastname}, {firstname}, {phone}, {email}, {branch_id}, NOW(), 1, {password});''')
            con.commit()
            resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, 'error', "" ,action)
    return resp


@csrf_exempt
def main(request):
    jsond = json.loads(request.body)
    action = jsond.get('action', 'nokey')
    resp = "Working not fine"
    if action == "login":
        resp = login(request)
    if action == "register":
        resp = register(request)
    if action == "list_category":
        resp = list_category(request)
    if action == "list_sub_category":
        resp = list_sub_category(request)
    if action == "add_category":
        resp = add_category(request)
    if action == "add_sub_category":
        resp = add_sub_category(request)
    if action == "edit_category":
        resp = edit_category(request)
    if action == "edit_sub_category":
        resp = edit_sub_category(request)
    if action == "delete_sub_category":
        resp = delete_sub_category(request)
    if action == "delete_category":
        resp = delete_category(request)
    
    
    
    return HttpResponse(resp)
























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


