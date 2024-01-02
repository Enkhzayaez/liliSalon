from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import UploadedFile
import dateutil.parser as dt
import requests
import json
from django.core.files.uploadedfile import InMemoryUploadedFile
import base64

BE_URL = "http://127.0.0.1:8080"
# Create your views here.

selectedServices = []

def index(request):
    context = {}
    if request.method == "GET":
        jsons = {
            "action" : "list_occupation",
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['occupations'] = result['data']
        jsons = {
            "action" : "list_sales",
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['sales'] = result['data']
    return render(request, 'index.html',context)

def services(request,occ_id = None):
    context = {}
    if request.method == "POST":
        # jsons = {
        #     "action" : "add_service",
        #     "name" : "",
        #     "occupation_id" : "",
        #     "price" : "",
        # }
        # jsons['name'] = request.POST.get('name')
        # jsons['occupation_id'] = request.POST.get('occupation_id')
        # jsons['price'] = request.POST.get('price')
        # con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        # result = json.loads(con.text)
        # context['errorMessage'] = result['data']
        return redirect('services')
    else:
        jsons = {
            "action" : "get_occupation",
            "id" : occ_id,
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['occupation'] = result['data']
        jsons = {
            "action" : "get_occ_service",
            "occ_id" : occ_id,
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['services'] = result['data']
    print(context)
    return render(request, 'services.html',context)


orders = {
    "selectedBranchName" : "",
    "selectedService" : "",
    "selectedWorker" : "",
    "selectedWorkers" : [],
    
    "selectedBranchId" : "",
    "selectedTime" : "",
    "selectedDate" : "",
    "total" : 0
}


def order(request):
    context = {'timelist' : ["8", "9", "11", "14", "15", "17", "18"]}
    if request.method == 'POST':
        jsons = {
        "action" : "get_branch",
        "id" : orders['selectedBranchId'],
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        selBranch = result['data'][0]['id']
        jsons = {
        "action" : "get_worker",
        "id" : orders['selectedWorker'],
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        selWorker = result['data'][0]['id']
        jsons = {
            "action" : "add_order",
            "service_id" : selectedServices,
            "worker_id" : selWorker,
            "order_date" : str(dt.parse(request.POST.get('selectedDate'))),
            "order_time" : str(request.POST.get('selectedTime')),
            "branch_id" : selBranch,
            "total_price" : orders["total"],
        }
      
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        jsons = {
            "action" : "get_last_order",
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['last_order'] = result['data']
        orders['selectedService'] = ""
        orders["selectedBranchName"] = ""
        orders["selectedWorker"] = ""
        orders["selectedWorkers"] = []
        orders["selectedBranchId"] = ""
        orders["selectedTime"] = ""
        orders["selectedDate"] = ""
        selectedServices.clear()
        orders["total"] = 0
        return redirect('order_confirm',result['data'][0]['id'])
    else:
        if request.GET.get('selectedBranchName') == None and request.GET.get('selectedService') and request.GET.get('selectedWorker') and request.GET.get('selectedDate') and request.GET.get('selectedTime'):
            orders["total"] = 0
        if request.GET.get('selectedBranchName'):
            jsons = {
            "action" : "get_branch",
            "id" : request.GET.get('selectedBranchName'),
            }
            con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
            result = json.loads(con.text)
            
            context['selectedBranchName'] = result['data'][0]['name']
            orders['selectedBranchName'] = result['data'][0]['name']
            orders['selectedBranchId'] = result['data'][0]['id']
        context['selectedBranchName'] = orders['selectedBranchName']
        if request.GET.get('selectedService'):
            context['selectedService'] = request.GET.get('selectedService')
            orders['selectedService'] = request.GET.get('selectedService')
            jsons = {
            "action" : "get_service",
            "id" : request.GET.get('selectedService'),
            }
            con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
            result = json.loads(con.text)
            selectedServices.append(result['data'])
        context['selectedServices'] = selectedServices
        if request.GET.get('selectedWorker'):
            context['selectedWorker'] = request.GET.get('selectedWorker')
            orders['selectedWorker'] = request.GET.get('selectedWorker')
            jsons = {
            "action" : "get_worker",
            "id" : request.GET.get('selectedWorker'),
            }
            con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
            result = json.loads(con.text)
            context['selectedWorker'] = result['data']
            orders['selectedWorkers'].append(context["selectedWorker"][0]['firstname'])
        if request.GET.get('selectedDate') and request.GET.get('selectedTime'):
            context['selectedDate'] = request.GET.get('selectedDate')
            context['selectedTime'] = request.GET.get('selectedTime')

            orders['selectedDate'] = request.GET.get('selectedDate')
            orders['selectedTime'] = request.GET.get('selectedTime')

        jsons = {
            "action" : "list_service",
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['services'] = result['data']
        jsons = {
            "action" : "list_branch",
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['branches'] = result['data']
        jsons = {
            "action" : "list_worker",
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['workers'] = result['data']
        jsons = {
            "action" : "list_order",
            }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['allorder'] = result['data']
        if context['selectedServices']:
            for service in context['selectedServices']:
                if service[0]['price']:
                    orders["total"] += service[0]['price']
                context['total'] = orders["total"]
    context['orders'] = orders
    return render(request, 'order.html',context)

def order_confirm(request, order_id=None):
    
    context = {}
    if order_id == 0:
        context["order_id"] = 'Order_Done'
        return render(request,'order_confirm.html',context)
    context['order_id'] = order_id
    if request.method == "POST":
        jsons = {
            "action" : "add_user",
            "phone" : "",
            "name" : "",
            "order_id" : "",
        }
        jsons['phone'] = request.POST.get("phone")
        jsons['name'] = request.POST.get("name")
        jsons['order_id'] = order_id
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        return redirect('index')
    return render(request,'order_confirm.html',context)

def adminEdit(request):
    return render(request, 'admin/adminEdit.html')

# Operator Edit lists
def list_operator(request):
    context = {}
    if request.method == "POST":
        jsons = {
            "action" : "add_operator",
            "lastname" : "",
            "firstname" : "",
            "phone" : "",
            "password" : "",
            "email" : "",
            "branch_id" : "",
            "admin_id" : "1",
        }
        jsons['lastname'] = request.POST.get('lastname')
        jsons['firstname'] = request.POST.get('firstname')
        jsons['phone'] = request.POST.get('phone')
        jsons['password'] = request.POST.get('password')
        jsons['email'] = request.POST.get('email')
        jsons['branch_id'] = request.POST.get('branch_id')
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['errorMessage'] = result['data']
        return redirect('list_operator')
    else:
        jsons = {
            "action" : "list_operator",
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['operators'] = result['data']
        jsons = {
            "action" : "list_branch",
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['branches'] = result['data']
    return render(request, 'lists/list_operator.html',context)

def delete_operator(request,operator_id = None):
    context = {}
    jsons = {
        "action" : "delete_operator",
        "id" : operator_id,
    }
    con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
    result = json.loads(con.text)
    context['errorMessage'] = result['data']
    return redirect('list_operator')

def list_services(request):
    context = {}
    if request.method == "POST":
        jsons = {
            "action" : "add_service",
            "name" : "",
            "occupation_id" : "",
            "price" : "",
        }
        jsons['name'] = request.POST.get('name')
        jsons['occupation_id'] = request.POST.get('occupation_id')
        jsons['price'] = request.POST.get('price')
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['errorMessage'] = result['data']
        return redirect('list_services')
    else:
        jsons = {
            "action" : "list_service",
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['services'] = result['data']
        jsons = {
            "action" : "list_occupation",
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['occupations'] = result['data']
    return render(request, 'lists/list_services.html',context)

def delete_service(request,service_id = None):
    context = {}
    jsons = {
        "action" : "delete_service",
        "id" : service_id,
    }
    con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
    result = json.loads(con.text)
    context['errorMessage'] = result['data']

    return redirect('list_services')

def edit_service(request,service_id = None):
    context = {}
    if request.method == "POST":
        jsons = {
            "action" : "edit_service",
            "name" : "",
            "price" : "",
            "ocupation_id" : "",
            "id" : service_id,
        }
        jsons['name'] = request.POST.get('name')
        jsons['price'] = request.POST.get('price')
        jsons['ocupation_id'] = request.POST.get('occupation_id') 
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['errorMessage'] = result['data']
        return redirect('list_services')
    else:
        jsons = {
            "action" : "get_service",
            "id" : service_id,
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['service'] = result['data'][0]
        jsons = {
            "action" : "list_occupation",
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['occupations'] = result['data']
    return render(request, 'editPages/edit_services.html',context)


def list_sales(request):
    context = {}
    if request.method == "POST":
        jsons = {
            "action" : "add_sales",
            "image" : "",
            "description" : "",
            "end_date" : "",
        }
        img = request.FILES.get('image')
        if not isinstance(img, InMemoryUploadedFile):
            raise ValueError("Input must be an InMemoryUploadedFile")
        base64_encoded = base64.b64encode(img.read()).decode('utf-8')
        jsons['image'] = base64_encoded
        jsons['description'] = request.POST.get('description')
        jsons['end_date'] = request.POST.get('end_date')
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['errorMessage'] = result['data']
        
        return redirect('list_sales')
    else:
        jsons = {
            "action" : "list_sales",
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['sales'] = result['data']
    return render(request, 'lists/list_sales.html',context)

def list_location(request):
    context = {}
    if request.method == "POST":
        jsons = {
            "action" : "add_branch",
            "name" : "",
            "address" : "",
            "phone" : "",
        }
        jsons['address'] = request.POST.get('address')
        jsons['name'] = request.POST.get('name')
        jsons['phone'] = request.POST.get('phone')
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['errorMessage'] = result['data']
        return redirect('list_location')
    else:
        jsons = {
            "action" : "list_branch",
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        
        context['branches'] = result['data']
    return render(request, 'lists/list_location.html',context)

def delete_location(request,branch_id = None):
    context = {}
    jsons = {
        "action" : "delete_branch",
        "id" : branch_id,
    }
    con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
    result = json.loads(con.text)
    context['errorMessage'] = result['data']

    return redirect('list_location')

def delete_workers(request,worker_id = None):
    context = {}
    jsons = {
        "action" : "delete_worker",
        "id" : worker_id,
    }
    con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
    result = json.loads(con.text)
    context['errorMessage'] = result['data']

    return redirect('list_workers')

def delete_occupation(request,occupation_id = None):
    context = {}
    jsons = {
        "action" : "delete_occupation",
        "id" : occupation_id,
    }
    con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
    result = json.loads(con.text)
    context['errorMessage'] = result['data']

    return redirect('list_occupation')

def list_orderlist(request):
    context = {}
    if request.method == "POST":
        return redirect('list_workers')
    else:
        jsons = {
            "action" : "list_order",
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['orders'] = result['data']
        jsons = {
            "action" : "list_service",
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['services'] = result['data']
        jsons = {
            "action" : "list_worker",
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['workers'] = result['data']
    print(context['orders'])
    return render(request, 'lists/list_orderlist.html',context)

def order_detail(request,phone = None):
    orders = [
        {   
            "order" : "Туяа",
            "phone" : 99554488,
            "date" : "2024/12/19 12:00:00",
            "services" : [
                {
                    "name" : "Nail art",
                    "price" : 150000,
                },
            ],
        },
        {
            "order" : "Батаа",
            "phone" : 80528787,
            "date" : "2024/02/07 16:00:00",
            "services" : [
                {
                    "name" : "Hair Styling",
                    "price" : 80000,
                },
                {
                    "name" : "Nail art",
                    "price" : 150000,
                },
            ],
        },
        {
            "order" : "Гэрлээ",
            "phone" : 99887799,
            "date" : "2024/06/01 14:00:00",
            "services" : [
                {
                    "name" : "Hair Shortening",
                    "price" : 25000,
                },
                {
                    "name" : "Hair Styling",
                    "price" : 80000,
                },
                {
                    "name" : "Nail art",
                    "price" : 150000,
                },
            ],
        },
    ]
    context = {'orders' : orders}
    for i in range(len(orders)):
        if orders[i]['phone'] == phone:
            context.update({"order" : orders[i]})
    
    return render(request, 'lists/order_details.html',context)

def list_workers(request):
    context = {}
    if request.method == "POST":
        jsons = {
            "action" : "add_worker",
            "lastname" : "",
            "firstname" : "",
            "phone" : "",
            "email" : "",
            "branch_id" : "",
            "occupation_id" : "",
        }
        jsons['lastname'] = request.POST.get('lastname')
        jsons['firstname'] = request.POST.get('firstname')
        jsons['phone'] = request.POST.get('phone')
        jsons['email'] = request.POST.get('email')
        jsons['branch_id'] = request.POST.get('branch_id')
        jsons['occupation_id'] = request.POST.get('occupation_id')
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['errorMessage'] = result['data']
        return redirect('list_workers')
    else:
        jsons = {
            "action" : "list_worker",
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['workers'] = result['data']
        jsons = {
            "action" : "list_branch",
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['branches'] = result['data']
        jsons = {
            "action" : "list_occupation",
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['occupations'] = result['data']
    return render(request, 'lists/list_workers.html',context)

def list_occupation(request):
    context = {}
    if request.method == "POST":
        
    
        jsons = {
            "action" : "add_occupation",
            "name" : "",
            "image" : ""
        }
        jsons['name'] = request.POST.get('name')
        img = request.FILES.get('image')
        if not isinstance(img, InMemoryUploadedFile):
            raise ValueError("Input must be an InMemoryUploadedFile")
        base64_encoded = base64.b64encode(img.read()).decode('utf-8')
        jsons['image'] = base64_encoded
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['errorMessage'] = result['data']
        return redirect('list_occupation')
    else:
        jsons = {
            "action" : "list_occupation",
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['occupations'] = result['data']
    return render(request, 'lists/list_occupation.html',context)

# Edit Pages
def edit_operator(request,operator_id = None):
    context = {}
    if request.method == "POST":
        jsons = {
            "action" : "edit_operator",
            "lastname" : "",
            "firstname" : "",
            "phone" : "",
            "password" : "",
            "email" : "",
            "branch_id" : "",
            "id" : operator_id,
        }
        jsons['lastname'] = request.POST.get('lastname')
        jsons['firstname'] = request.POST.get('firstname')
        jsons['phone'] = request.POST.get('phone')
        jsons['password'] = request.POST.get('password') 
        jsons['email'] = request.POST.get('email')
        jsons['branch_id'] = request.POST.get('branch_id')
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['errorMessage'] = result['data']
        return redirect('list_operator')
    else:
        jsons = {
            "action" : "get_operator",
            "id" : operator_id,
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['operator'] = result['data'][0]
    return render(request, 'editPages/edit_operator.html',context)

def edit_occupation(request,occupation_id = None):
    context = {}
    if request.method == "POST":
        jsons = {
            "action" : "edit_occupation",
            "name" : "",
            "id" : occupation_id,
            "image" : ""
        }
        img = request.FILES.get('image')
        if img == None:
            jsons["image"] = request.POST.get("oldImage")
        else:
            if not isinstance(img, InMemoryUploadedFile):
                raise ValueError("Input must be an InMemoryUploadedFile")
            base64_encoded = base64.b64encode(img.read()).decode('utf-8')
            jsons['image'] = base64_encoded
        jsons['name'] = request.POST.get('name')
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['errorMessage'] = result['data']
        return redirect('list_occupation')
    else:
        jsons = {
            "action" : "get_occupation",
            "id" : occupation_id,
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['occupation'] = result['data'][0]
    return render(request, 'editPages/edit_occupation.html',context)


def edit_services(request):
    return render(request, 'editPages/edit_services.html')

def edit_sales(request,sale_id = None):
    return render(request, 'editPages/edit_sales.html')

def edit_location(request,branch_id = None):
    context = {}
    if request.method == "POST":
        jsons = {
            "action" : "edit_branch",
            "address" : "",
            "phone" : "",
            "name" : "",
            "id" : branch_id,
            "new_id" : ""
        }
        jsons['address'] = request.POST.get('address')
        jsons['phone'] = request.POST.get('phone')
        jsons['name'] = request.POST.get('name')
        jsons['new_id'] = request.POST.get('new_id')

        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['errorMessage'] = result['data']
        return redirect('list_location')
    else:
        jsons = {
            "action" : "get_branch",
            "id" : branch_id,
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['branch'] = result['data'][0]
    return render(request, 'editPages/edit_location.html',context)

def edit_order(request,order_id = None):
    context = {}
    if request.method == "POST":
        jsons = {
            "action" : "edit_branch",
            "address" : "",
            "phone" : "",
            "name" : "",
            "new_id" : ""
        }
        jsons['address'] = request.POST.get('address')
        jsons['phone'] = request.POST.get('phone')
        jsons['name'] = request.POST.get('name')
        jsons['new_id'] = request.POST.get('new_id')

        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['errorMessage'] = result['data']
        return redirect('list_location')
    else:
        jsons = {
            "action" : "get_branch",
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['branch'] = result['data'][0]
    return render(request, 'editPages/edit_order.html')

def delete_order(request,order_id = None):
    context = {}
    print(order_id)
    jsons = {
        "action" : "delete_order",
        "id" : order_id,
    }
    con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
    result = json.loads(con.text)
    context['errorMessage'] = result['data']

    return redirect('list_orderlist')

def delete_sales(request,sale_id = None):
    context = {}
    jsons = {
        "action" : "delete_sales",
        "id" : sale_id,
    }
    con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
    result = json.loads(con.text)
    context['errorMessage'] = result['data']
    return redirect('list_sales')

def edit_sales(request,sale_id = None):
    context = {}
    if request.method == "POST":
        jsons = {
            "action" : "edit_sales",
            "image" : "",
            "description" : "",
            "end_date" : "",
            "id" : sale_id,
        }
        jsons['description'] = request.POST.get('description')
        
        jsons['end_date'] = request.POST.get('end_date')
        print(jsons['end_date'])
        img = request.FILES.get('image')
        if img == None:
            jsons["image"] = request.POST.get("oldImage")
        else:
            if not isinstance(img, InMemoryUploadedFile):
                raise ValueError("Input must be an InMemoryUploadedFile")
            base64_encoded = base64.b64encode(img.read()).decode('utf-8')
            jsons['image'] = base64_encoded
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['errorMessage'] = result['data']
        return redirect('list_sales')
    else:
        jsons = {
            "action" : "get_sales",
            "id" : sale_id,
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['sales'] = result['data'][0]
    return render(request, 'editPages/edit_sales.html',context)


def edit_workers(request,worker_id = None):
    context = {}
    if request.method == "POST":
        jsons = {
            "action" : "edit_worker",
            "lastname" : "",
            "firstname" : "",
            "phone" : "",
            "email" : "",
            "branch_id" : "",
            "occupation_id" : "",
            "id" : worker_id,
        }
        jsons['lastname'] = request.POST.get('lastname')
        jsons['firstname'] = request.POST.get('firstname')
        jsons['phone'] = request.POST.get('phone')
        jsons['email'] = request.POST.get('email')
        jsons['branch_id'] = request.POST.get('branch_id')
        jsons['occupation_id'] = request.POST.get('occupation_id') 
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        print(con.text)
        result = json.loads(con.text)
        context['errorMessage'] = result['data']
        return redirect('list_workers')
    else:
        jsons = {
            "action" : "get_worker",
            "id" : worker_id,
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['worker'] = result['data'][0]
        jsons = {
            "action" : "list_branch",
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['branches'] = result['data']
        jsons = {
            "action" : "list_occupation",
        }
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        context['occupations'] = result['data']
    return render(request, 'editPages/edit_workers.html',context)

# Add Pages
def add_operator(request):
    return render(request, 'addPages/add_operator.html')

def add_services(request):
    return render(request, 'addPages/add_services.html')

def add_sales(request):
    return render(request, 'addPages/add_sales.html')

def add_location(request):
    return render(request, 'addPages/add_location.html')

def add_orderlist(request):
    return render(request, 'addPages/add_orderlist.html')

def add_workers(request):
    return render(request, 'addPages/add_workers.html')

def a_location(request):
    return render(request, 'admin/a_location.html')

def operator(request):
    context = {
        'data' :
        [
            {
                'name' : 'Үйлчилгээ' ,'image' : '../../static/images/full.jpg', 'path': 'list_services'
            },
              {
                'name' : 'Салбар' ,'image' : '../../static/images/full.jpg','path': 'list_location'
            },
              {
                'name' : 'Хөнгөлөлт' ,'image' : '../../static/images/full.jpg','path': 'list_sales'
            },
              {
                'name' : 'Захиалгууд' ,'image' : '../../static/images/full.jpg','path': 'list_orderlist'
            },
              {
                'name' : 'Мэргэжил' ,'image' : '../../static/images/full.jpg','path': 'list_occupation'
            },
              {
                'name' : 'Ажилтан' ,'image' : '../../static/images/full.jpg','path': 'list_workers'
            },
            
        ]
    }
    return render(request, 'operator/operator.html',context)

@login_required(login_url="login")
def logout(request):
    if request.method =="GET":
        auth.logout(request=request)
    return redirect('login')

def login(request):
    if request.method == "POST":
        jsons = {
            "action" : "login",
            "phone" : "",
            "password": "",
        }
        jsons['password'] = request.POST.get('password') 
        jsons['phone'] = request.POST.get('phone')
        con = requests.post(f"{BE_URL}", data= json.dumps(jsons))
        result = json.loads(con.text)
        if result['resultCode'] == 200:
            if result['resultMessege'] == 'admin':
                return redirect("adminEdit")
            else: 
                return redirect('operator')
        else:
            return render(request, 'signUp/login.html')
    else:
        return render(request, 'signUp/login.html')
    
def hairStyle(request):
    return render(request, 'hairStyle.html')

