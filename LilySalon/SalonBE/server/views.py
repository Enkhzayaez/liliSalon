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

def get_operator(request):
    jsond = json.loads(request.body)
    action = jsond.get("action")
    id = jsond.get("id")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute('''SELECT * FROM t_operator WHERE id = %s;''',[id])
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
    image = jsond.get("image")
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(f'''SELECT * FROM t_operator WHERE email = '{email}' OR phone = '{phone}';''')
        cat = cur.fetchall()
        if cat != []:
            resp = sendResponse(402, 'already operator with same email or phone', "" ,action)
        else:
            cur.execute('''INSERT INTO t_operator(
                            id, lastname, firstname, phone, email, password, regdate, admin_id, branch_id, image)
                            VALUES (DEFAULT, %s, %s, %s, %s, %s, NOW(), %s, %s, %s);''',[lastname,firstname,phone,email,password,admin_id,branch_id,image])
            con.commit()
            resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, str(e), "" ,action)
    return resp

def edit_operator(request):
    jsond = json.loads(request.body)
    lastname = jsond.get("lastname")
    firstname = jsond.get("firstname")
    phone = jsond.get("phone")
    email = jsond.get("email")
    branch_id = jsond.get("branch_id")
    password = jsond.get("password")
    id = jsond.get("id")
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:

        cur.execute(''' UPDATE t_operator
                        SET lastname=%s, firstname=%s, phone=%s, email=%s, password=%s, branch_id=%s
                        WHERE id = %s;''',[lastname,firstname,phone,email,password,branch_id,id])
        con.commit()
        resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, str(e), "" ,action)
    return resp

def delete_operator(request):
    jsond = json.loads(request.body)
    id = jsond.get("id")
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(''' DELETE FROM t_operator
	                    WHERE id = %s;''',[id])
        con.commit()
        resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, str(e), "" ,action)
    return resp

def list_branch(request):
    jsond = json.loads(request.body)
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(f'''SELECT * FROM t_branch;''')
        columns = cur.description
        respRow = [{columns[index][0]:column for index,
                    column in enumerate(value)} for value in cur.fetchall()]
        resp = sendResponse(200, 'success', respRow ,  action)
    except Exception as e:
        resp = sendResponse(401, 'error', "" ,action)
    return resp

def get_branch(request):
    jsond = json.loads(request.body)
    action = jsond.get("action")
    id = jsond.get("id")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute('''SELECT * FROM t_branch WHERE id = %s;''',[id])
        columns = cur.description
        respRow = [{columns[index][0]:column for index,
                    column in enumerate(value)} for value in cur.fetchall()]
        resp = sendResponse(200, 'success', respRow ,  action)
    except Exception as e:
        resp = sendResponse(401, str(e), "" ,action)
    return resp

def add_branch(request):
    jsond = json.loads(request.body)
    name = jsond.get("name")
    address = jsond.get("address")
    phone = jsond.get("phone")
    image = jsond.get("image")
    action = jsond.get("action")
    
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(''' INSERT INTO t_branch(
                        id, name, address, phone,image)
                        VALUES (DEFAULT, %s, %s, %s, %s);''',[name,address,phone,image])
        con.commit()
        resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, str(e), "" ,action)
    return resp

def edit_branch(request):
    jsond = json.loads(request.body)
    name = jsond.get("name")
    address = jsond.get("address")
    phone = jsond.get("phone")
    new_id = jsond.get("new_id")
    id = jsond.get('id')
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(''' UPDATE t_branch
                        SET id=%s, name=%s, address=%s, phone=%s
                        WHERE id=%s;''',[new_id,name,address,phone,id])
        con.commit()
        resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, str(e), "" ,action)
    return resp

def delete_branch(request):
    jsond = json.loads(request.body)
    id = jsond.get("id")
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(''' DELETE FROM t_branch
	                    WHERE id = %s;''',[id])
        con.commit()
        resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, str(e), "" ,action)
    return resp

def list_worker(request):
    jsond = json.loads(request.body)
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(f'''SELECT * FROM t_worker;''')
        columns = cur.description
        respRow = [{columns[index][0]:column for index,
                    column in enumerate(value)} for value in cur.fetchall()]
        resp = sendResponse(200, 'success', respRow ,  action)
    except Exception as e:
        resp = sendResponse(401, 'error', "" ,action)
    return resp

def get_worker(request):
    jsond = json.loads(request.body)
    action = jsond.get("action")
    id = jsond.get("id")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute('''SELECT * FROM t_worker WHERE id = %s;''',[id])
        columns = cur.description
        respRow = [{columns[index][0]:column for index,
                    column in enumerate(value)} for value in cur.fetchall()]
        resp = sendResponse(200, 'success', respRow ,  action)
    except Exception as e:
        resp = sendResponse(401, 'error', "" ,action)
    return resp

def add_worker(request):
    jsond = json.loads(request.body)
    lastname = jsond.get("lastname")
    firstname = jsond.get("firstname")
    phone = jsond.get("phone")
    email = jsond.get("email")
    branch_id = jsond.get("branch_id")
    occupation_id = jsond.get("occupation_id")
    image = jsond.get("image")
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(''' INSERT INTO t_worker(
                        id, lastname, firstname, phone, email, regdate, branch_id, ocupation_id, image)
                        VALUES (DEFAULT, %s, %s, %s, %s, NOW(), %s, %s, %s);''',[lastname,firstname,phone,email,branch_id,occupation_id,image])
        con.commit()
        resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, str(e), "" ,action)
    return resp

def edit_worker(request):
    jsond = json.loads(request.body)
    firstname = jsond.get("firstname")
    lastname = jsond.get("lastname")
    phone = jsond.get("phone")
    email = jsond.get("email")
    occupation_id = jsond.get('occupation_id')
    branch_id = jsond.get('branch_id')
    id = jsond.get('id')
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(''' UPDATE t_worker
                        SET lastname=%s, firstname=%s, phone=%s, email=%s, branch_id=%s, ocupation_id=%s
                        WHERE id = %s;''',[lastname,firstname,phone,email,branch_id,occupation_id,id])
        con.commit()
        resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, str(e), "" ,action)
    return resp

def delete_worker(request):
    jsond = json.loads(request.body)
    id = jsond.get("id")
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(''' DELETE FROM t_worker
	                    WHERE id = %s;''',[id])
        con.commit()
        resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, str(e), "" ,action)
    return resp

def list_occupation(request):
    jsond = json.loads(request.body)
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(f'''SELECT * FROM t_ocupation;''')
        columns = cur.description
        respRow = [{columns[index][0]:column for index,
                    column in enumerate(value)} for value in cur.fetchall()]
        resp = sendResponse(200, 'success', respRow ,  action)
    except Exception as e:
        resp = sendResponse(401, 'error', "" ,action)
    return resp

def get_occupation(request):
    jsond = json.loads(request.body)
    action = jsond.get("action")
    id = jsond.get("id")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute('''SELECT * FROM t_ocupation WHERE id = %s;''',[id])
        columns = cur.description
        respRow = [{columns[index][0]:column for index,
                    column in enumerate(value)} for value in cur.fetchall()]
        resp = sendResponse(200, 'success', respRow ,  action)
    except Exception as e:
        resp = sendResponse(401, 'error', "" ,action)
    return resp

def add_occupation(request):
    jsond = json.loads(request.body)
    name = jsond.get("name")
    image = jsond.get("image")
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(''' INSERT INTO t_ocupation(
                        id, name, image)
                        VALUES (DEFAULT, %s, %s);''',[name,image])
        con.commit()
        resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, str(e), "" ,action)
    return resp

def edit_occupation(request):
    jsond = json.loads(request.body)
    name = jsond.get("name")
    id = jsond.get('id')
    image = jsond.get('image')
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(''' UPDATE t_ocupation
                        SET name=%s , image=%s
                        WHERE id=%s;''',[name,image,id])
        con.commit()
        resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, str(e), "" ,action)
    return resp

def delete_occupation(request):
    jsond = json.loads(request.body)
    id = jsond.get("id")
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(''' DELETE FROM t_ocupation
	                    WHERE id = %s;''',[id])
        con.commit()
        resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, str(e), "" ,action)
    return resp

def list_service(request):
    jsond = json.loads(request.body)
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(f'''SELECT * FROM t_service;''')
        columns = cur.description
        respRow = [{columns[index][0]:column for index,
                    column in enumerate(value)} for value in cur.fetchall()]
        resp = sendResponse(200, 'success', respRow ,  action)
    except Exception as e:
        resp = sendResponse(401, 'error', "" ,action)
    return resp

def get_service(request):
    jsond = json.loads(request.body)
    action = jsond.get("action")
    id = jsond.get("id")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute('''SELECT * FROM t_service WHERE id = %s;''',[id])
        columns = cur.description
        respRow = [{columns[index][0]:column for index,
                    column in enumerate(value)} for value in cur.fetchall()]
        resp = sendResponse(200, 'success', respRow ,  action)
    except Exception as e:
        resp = sendResponse(401, 'error', "" ,action)
    return resp

def add_service(request):
    jsond = json.loads(request.body)
    name = jsond.get("name")
    occupation_id = jsond.get("occupation_id")
    price = jsond.get("price")
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(''' INSERT INTO t_service(
                        id, category_id, name, price, ocupation_id)
                        VALUES (DEFAULT, 1, %s, %s, %s);''',[name,price,occupation_id])
        con.commit()
        resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, str(e), "" ,action)
    return resp

def edit_service(request):
    jsond = json.loads(request.body)
    name = jsond.get("name")
    ocupation_id = jsond.get("ocupation_id")
    price = jsond.get("price")
    id = jsond.get('id')
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(''' UPDATE t_service
                        SET name=%s,ocupation_id=%s,price=%s
                        WHERE id=%s;''',[name,ocupation_id,price,id])
        con.commit()
        resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, str(e), "" ,action)
    return resp

def delete_service(request):
    jsond = json.loads(request.body)
    id = jsond.get("id")
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(''' DELETE FROM t_service
	                    WHERE id = %s;''',[id])
        con.commit()
        resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, str(e), "" ,action)
    return resp

def list_order(request):
    jsond = json.loads(request.body)
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(f'''SELECT * FROM t_user INNER JOIN t_order ON t_user.id = t_order.user_id''')
        columns = cur.description
        respRow = [{columns[index][0]:column for index,
                    column in enumerate(value)} for value in cur.fetchall()]
        resp = sendResponse(200, 'success', respRow ,  action)
    except Exception as e:
        resp = sendResponse(401, 'error', "" ,action)
    return resp

def list_sales(request):
    jsond = json.loads(request.body)
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(f'''SELECT * FROM t_sale;''')
        columns = cur.description
        respRow = [{columns[index][0]:column for index,
                    column in enumerate(value)} for value in cur.fetchall()]
        resp = sendResponse(200, 'success', respRow ,  action)
    except Exception as e:
        resp = sendResponse(401, 'error', str(e) ,action)
    return resp

def edit_sales(request):
    jsond = json.loads(request.body)
    image = jsond.get("image")
    description = jsond.get("description")
    end_date = jsond.get("end_date")
    id = jsond.get("id")
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(''' UPDATE t_sale
                        SET image=%s,description=%s,end_date=%s
                        WHERE id=%s;''',[image,description,end_date,id])
        con.commit()
        
        resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, str(e), "" ,action)
    return resp

def get_sales(request):
    jsond = json.loads(request.body)
    action = jsond.get("action")
    id = jsond.get("id")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute('''SELECT * FROM t_sale WHERE id = %s;''',[id])
        columns = cur.description
        respRow = [{columns[index][0]:column for index,
                    column in enumerate(value)} for value in cur.fetchall()]
        resp = sendResponse(200, 'success', respRow ,  action)
    except Exception as e:
        resp = sendResponse(401, 'error', "" ,action)
    return resp

def delete_order(request):
    jsond = json.loads(request.body)
    id = jsond.get("id")
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(''' DELETE FROM t_order
	                    WHERE id = %s;''',[id])
        con.commit()
        resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, str(e), "" ,action)
    return resp

def delete_sales(request):
    jsond = json.loads(request.body)
    id = jsond.get("id")
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(''' DELETE FROM t_sale
	                    WHERE id = %s;''',[id])
        con.commit()
        resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, str(e), "" ,action)
    return resp

def add_order(request):
    jsond = json.loads(request.body)
    service_id = jsond.get("service_id")
    worker_id = jsond.get("worker_id")
    order_date = jsond.get("order_date")
    order_time = jsond.get("order_time")
    branch_id = jsond.get("branch_id")
    total_price = jsond.get("total_price")
    action = jsond.get("action")
    services = []
    print(order_time[0:2])
    for data in service_id[0]:
        services.append(data['id'])
    con = connect()
    cur = con.cursor()
    print([services,worker_id,order_date,order_time[0:2],branch_id,total_price])
    try:
        cur.execute(''' INSERT INTO t_order(
                        id, service_id, worker_id, order_date, order_time, branch_id, total_price)
                        VALUES (DEFAULT, %s, %s, %s, %s, %s, %s);''',
                        [services,worker_id,order_date,order_time[0:2],branch_id,total_price])
        con.commit()
        resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        print(e)
        resp = sendResponse(401, str(e), "" ,action)
    return resp
    
def get_last_order(request):
    jsond = json.loads(request.body)
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(f'''SELECT * FROM t_order ORDER BY id DESC LIMIT 1;''')
        columns = cur.description
        respRow = [{columns[index][0]:column for index,
                    column in enumerate(value)} for value in cur.fetchall()]
        resp = sendResponse(200, 'success', respRow ,  action)
    except Exception as e:
        resp = sendResponse(401, str(e), "" ,action)
    return resp

def add_user(request):
    jsond = json.loads(request.body)
    name = jsond.get("name")
    phone = jsond.get("phone")
    order_id = jsond.get("order_id")
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute('''SELECT * FROM t_user WHERE name=%s AND phone=%s''',[name,phone])
        columns = cur.description
        respRow = [{columns[index][0]:column for index,
                    column in enumerate(value)} for value in cur.fetchall()]
        if respRow == []:
            cur.execute(''' INSERT INTO t_user(
                            id, name, phone)
                            VALUES (DEFAULT, %s, %s);''',
                            [name, phone])
        con.commit()
        cur.execute('''SELECT id FROM t_user WHERE name=%s AND phone=%s''',[name,phone])
        columns = cur.description
        respRow = [{columns[index][0]:column for index,
                    column in enumerate(value)} for value in cur.fetchall()][0]
        cur.execute(''' UPDATE t_order
                        SET user_id=%s
                        WHERE id = %s;''',
                            [respRow['id'], order_id])
        con.commit()
        resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        print(e)
        resp = sendResponse(401, str(e), "" ,action)
    return resp
    
def add_sales(request):
    jsond = json.loads(request.body)
    image = jsond.get("image")
    description = jsond.get("description")
    end_date = jsond.get("end_date")
    action = jsond.get("action")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(''' INSERT INTO t_sale(
                        id, end_date, description, image)
                        VALUES (DEFAULT, %s, %s, %s);''',[end_date,description,image])
        con.commit()
        resp = sendResponse(200, 'success', "" ,action)
    except Exception as e:
        resp = sendResponse(401, str(e), "" ,action)
    return resp

def login(request):
    jsond = json.loads(request.body)
    action = jsond.get("action")
    phone = jsond.get("phone")
    password = jsond.get("password")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute('''SELECT * FROM t_operator WHERE phone = %s AND password = %s;''',[phone,password])
        message = 'operator'
        data = cur.fetchall()
        if data == []:
            cur.execute('''SELECT * FROM t_admin WHERE phone = %s AND password = %s;''',[phone,password])
            message = 'admin'
            data = cur.fetchall()
        columns = cur.description
        respRow = [{columns[index][0]:column for index,
                    column in enumerate(value)} for value in data]
        resp = sendResponse(200, message, respRow ,  action)
    except Exception as e:
        resp = sendResponse(401, 'error', "" ,action)
    return resp

def get_occ_service(request):
    jsond = json.loads(request.body)
    action = jsond.get("action")
    occ_id = jsond.get('occ_id')
    print(occ_id)
    con = connect()
    cur = con.cursor()
    try:
        cur.execute('''SELECT * FROM t_service WHERE ocupation_id = %s;''',[occ_id])
        columns = cur.description
        respRow = [{columns[index][0]:column for index,
                    column in enumerate(value)} for value in cur.fetchall()]
        
        resp = sendResponse(200, 'success', respRow ,  action)
        print(resp)
    except Exception as e:
        resp = sendResponse(401, str(e), str(e) ,action)
    return resp


@csrf_exempt
def main(request):
    jsond = json.loads(request.body)
    action = jsond.get('action')
    resp = sendResponse(401, 'working not fine', "" ,action)
    # operator
    if action == "add_operator":
        resp = add_operator(request)
    if action == "list_operator":
        resp = list_operator(request)    
    if action == "get_operator":
        resp = get_operator(request)   
    if action == "edit_operator":
        resp = edit_operator(request) 
    if action == "delete_operator":
        resp = delete_operator(request) 

    # branch
    if action == "add_branch":
        resp = add_branch(request)
    if action == "list_branch":
        resp = list_branch(request)    
    if action == "get_branch":
        resp = get_branch(request)   
    if action == "edit_branch":
        resp = edit_branch(request) 
    if action == "delete_branch":
        resp = delete_branch(request) 

    # worker
    if action == "add_worker":
        resp = add_worker(request)
    if action == "list_worker":
        resp = list_worker(request)    
    if action == "get_worker":
        resp = get_worker(request)   
    if action == "edit_worker":
        resp = edit_worker(request) 
    if action == "delete_worker":
        resp = delete_worker(request) 

    # occupation
    if action == "add_occupation":
        resp = add_occupation(request)
    if action == "list_occupation":
        resp = list_occupation(request)    
    if action == "get_occupation":
        resp = get_occupation(request)   
    if action == "edit_occupation":
        resp = edit_occupation(request) 
    if action == "delete_occupation":
        resp = delete_occupation(request)

    # service
    if action == "add_service":
        resp = add_service(request)
    if action == "list_service":
        resp = list_service(request)    
    if action == "get_service":
        resp = get_service(request)   
    if action == "edit_service":
        resp = edit_service(request) 
    if action == "delete_service":
        resp = delete_service(request)

    if action == "get_occ_service":
        resp = get_occ_service(request)

    # order
    if action == "add_order":
        resp = add_order(request)
    if action == "get_last_order":
        resp = get_last_order(request)
    if action == "list_order":
        resp = list_order(request)
    if action == "delete_order":
        resp = delete_order(request)

    # sales
    if action == "list_sales":
        resp = list_sales(request)
    if action == "add_sales":
        resp = add_sales(request)
    if action == "get_sales":
        resp = get_sales(request)
    if action == "delete_sales":
        resp = delete_sales(request)
    if action == "edit_sales":
        resp = edit_sales(request)

    # user
    if action == "add_user":
        resp = add_user(request)

    if action == "login":
        resp = login(request) 
    return HttpResponse(resp)