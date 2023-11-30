from django.http import HttpResponse
import json
import hashlib
from django.views.decorators.csrf import csrf_exempt
from server.utils import *


# Utils
def login(request):
    jsond = json.loads(request.body)
    action = jsond.get('action')
    phone = jsond.get('phone')
    password = jsond.get('password')
    password = mandakhHash(password)
    con = connect()
    cursor = con.cursor()
    cursor.execute(f"""SELECT * FROM t_operator WHERE phone = '{phone}' AND password = '{password}' """)
    columns = cursor.description
    respRow = [{columns[index][0]:column for index,
                column in enumerate(value)} for value in cursor.fetchall()]
    if len(respRow) == 1:
        resp = sendResponse(200, 'success', respRow ,  action)
        return resp
    else:
        resp = sendResponse(400, 'error', "" ,action)
        return resp
    
def register(request):
    try:
        jsond = json.loads(request.body)
        action = jsond.get('action')
        phone = jsond.get('phone')
        password = jsond.get('password')
        lastname = jsond.get('lastname')
        firstname = jsond.get('firstname')
        branch_id = jsond.get('branch_id')
        email = jsond.get('email')
        password = mandakhHash(password)
        con = connect()
        cursor = con.cursor()
        cursor.execute(f"""SELECT * FROM t_operator WHERE phone = '{phone}' AND email = '{email}';""")
        temp_checker = cursor.fetchall()
    
        if not temp_checker:
            cursor.execute(""" INSERT INTO t_operator(
                                id, lastname, firstname, phone, email, branch_id, reg_date, is_active, password)
                                VALUES (DEFAULT, %s, %s, %s, %s, %s, DEFAULT, DEFAULT, %s);""",[lastname,firstname,phone,email,branch_id,password])
            con.commit()
            resp = sendResponse(200, 'success', "" ,action)
            return resp
        else:
            resp = sendResponse(404, 'there is user with credentials in system', "" ,action)
            return resp
    except Exception as e:
        resp = sendResponse(404, e, "" ,action)
        return resp

# Add
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
    phone = jsond.get("phone")
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(f'''SELECT * FROM t_branch WHERE address = '{address}';''')
        cat = cur.fetchall()
        if cat  != []:
            resp = sendResponse(402, 'already branch with same address', "" ,action)
        else:
            cur.execute('''INSERT INTO t_branch(
                            id, address, operator_id,phone, image)
                            VALUES (DEFAULT, %s, %s, %s, %s);''',(address,operator_id,phone,['Nothing']))
            con.commit()
            resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, 'error', e ,action)
    return resp

def add_services(request):
    try:
        jsond = json.loads(request.body)
        action = jsond.get('action')
        name = jsond.get('name')
        sub_category_id = jsond.get('sub_category_id')
        category_id = jsond.get('category_id')
        description = jsond.get('description')
        options = jsond.get('options')
        additional = jsond.get('additional')
        con = connect()
        cursor = con.cursor()
        cursor.execute("""  INSERT INTO t_services(
                            id, name, sub_category_id, category_id, description, options, additional)
                            VALUES (DEFAULT, %s, %s, %s, %s, %s, %s);""",[name,sub_category_id,category_id,description,json.dumps(options),additional])
        con.commit()
        resp = sendResponse(200, 'success', "" ,action)
        return resp
    except Exception as e:
        resp = sendResponse(404, e, "" ,action)
        return resp

# List
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

def list_operator(request):
    jsons = json.loads(request.body)
    action = jsons.get('action')
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(f'''SELECT * FROM t_operator;''')
        columns = cur.description
        respRow = [{columns[index][0]:column for index,
                    column in enumerate(value)} for value in cur.fetchall()]
        resp = sendResponse(200, 'success', respRow,  action)
    except Exception as e:
        resp = sendResponse(401, 'error', str(e) ,action)
    return resp

def list_services(request):
    jsons = json.loads(request.body)
    action = jsons.get('action')
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(f'''SELECT * FROM t_services;''')
        columns = cur.description
        respRow = [{columns[index][0]:column for index,
                    column in enumerate(value)} for value in cur.fetchall()]
        resp = sendResponse(200, 'success', respRow,  action)
    except Exception as e:
        resp = sendResponse(401, 'error', str(e) ,action)
    return resp

# Edit
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
    phone = jsond.get("phone")
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
            cur.execute('''UPDATE t_branch
                            SET address= %s , phone= %s 
                            WHERE id = %s;''',[address,phone,id])
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

def edit_operator(request):
    try:
        jsond = json.loads(request.body)
        action = jsond.get('action')
        phone = jsond.get('phone')
        password = jsond.get('password')
        lastname = jsond.get('lastname')
        firstname = jsond.get('firstname')
        branch_id = jsond.get('branch_id')
        email = jsond.get('email')
        id = jsond.get('id')
        password = mandakhHash(password)
        con = connect()
        cur = con.cursor()
        try:
            cur.execute(f'''SELECT * FROM t_operator WHERE id = '{id}';''')
            cat = cur.fetchall()
            if cat == []:
                resp = sendResponse(402, 'no operator found', "" ,action)
            else:
                cur.execute('''UPDATE t_operator
                                SET lastname = %s, firstname = %s, phone = %s, email = %s,
                                branch_id = %s, password = %s 
                                WHERE id = %s;''',[lastname,firstname,phone,email,branch_id,password,id]) 
                con.commit()
                resp = sendResponse(200, 'success', "" ,action)
        except Exception as e:
            resp = sendResponse(401, 'error', e ,action)
    except Exception as e:
        resp = sendResponse(404, e, "" ,action)
    return resp

# Delete
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

def delete_branch(request):
    jsond = json.loads(request.body)
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
            cur.execute(f'''DELETE FROM t_branch
	                        WHERE id = {id};''')
            con.commit()
            resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, 'error', e ,action)
    return resp

def delete_operator(request):
    jsond = json.loads(request.body)
    id = jsond.get("id")
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(f'''SELECT * FROM t_operator WHERE id = '{id}';''')
        cat = cur.fetchall()
        if cat == []:
            resp = sendResponse(402, 'no operator found', "" ,action)
        else:
            cur.execute(f'''DELETE FROM t_operator
	                        WHERE id = {id};''')
            con.commit()
            resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, 'error', e ,action)
    return resp

# Get
def get_operator(request):
    jsons = json.loads(request.body)
    action = jsons.get('action')
    id = jsons.get('id')
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(f'''SELECT * FROM t_operator WHERE id = '{id}';''')
        columns = cur.description
        respRow = [{columns[index][0]:column for index,
                    column in enumerate(value)} for value in cur.fetchall()]
        resp = sendResponse(200, 'success', respRow,  action)
    except Exception as e:
        resp = sendResponse(401, 'error', str(e) ,action)
    return resp

def get_branch(request):
    jsons = json.loads(request.body)
    action = jsons.get('action')
    id = jsons.get('id')
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(f'''SELECT * FROM t_branch WHERE id = '{id}';''')
        columns = cur.description
        respRow = [{columns[index][0]:column for index,
                    column in enumerate(value)} for value in cur.fetchall()]
        resp = sendResponse(200, 'success', respRow,  action)
    except Exception as e:
        resp = sendResponse(401, 'error', str(e) ,action)
    return resp


@csrf_exempt
def main(request):
    jsond = json.loads(request.body)
    action = jsond.get('action', 'nokey')
    resp = "Working not fine"
    # Utils
    if action == "login":
        resp = login(request)
    if action == "register":
        resp = register(request)

    # List
    if action == "list_category":
        resp = list_category(request)
    if action == "list_sub_category":
        resp = list_sub_category(request)
    if action == "list_branch":
        resp = list_branch(request)
    if action == "list_operator":
        resp = list_operator(request)
    if action == "list_services":
        resp = list_services(request)

    # Add
    if action == "add_category":
        resp = add_category(request)
    if action == "add_sub_category":
        resp = add_sub_category(request)
    if action == "add_branch":
        resp = add_branch(request)
    if action == "add_services":
        resp = add_services(request)

    # Edit
    if action == "edit_category":
        resp = edit_category(request)
    if action == "edit_sub_category":
        resp = edit_sub_category(request)
    if action == "edit_branch":
        resp = edit_branch(request)
    if action == "edit_operator":
        resp = edit_operator(request)

    # Delete
    if action == "delete_sub_category":
        resp = delete_sub_category(request)
    if action == "delete_category":
        resp = delete_category(request)
    if action == "delete_branch":
        resp = delete_branch(request)
    if action == "delete_operator":
        resp = delete_operator(request)

    # Get
    if action == "get_operator":
        resp = get_operator(request)
    if action == "get_branch":
        resp = get_branch(request)

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


