from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import requests
import json
BE_URL = "http://127.0.0.1:8080"
# Create your views here.

orders = {
        'services' : [],
        'worker': "",
        'location': "",
    }
def index(request):
    return render(request, 'index.html')

def services(request):
    return render(request, 'services.html')

def order(request):
    branches = [
        'Sydney',
        'London',
        'UK',
        'USA',
        'Japan',
    ]
    serviceDatas = [
        ['Hair coloring',15000],
        ['Nail polishing',25000],
        ['Hair styling',85000],
        ['Manecure',64000],
        ['Hair something',999999],
    ]

    workers = [
        'Bob',
        'John',
        'Kyrie',
        'Sarah',
        'Michele',
    ]

    
    if request.method == 'POST':
        if request.POST.get('selectedBranch'):
            orders['location'] = request.POST.get('selectedBranch')
    
        if request.POST.get('selectedService'):
            for i in range(len(serviceDatas)):
                if(serviceDatas[i][0] == request.POST.get('selectedService')):
                    orders['services'].append(serviceDatas[i])
        
    context = {
        'services' : serviceDatas,
        'orders' : orders,
        'branches' : branches,
    }
    
    return render(request, 'order.html',context)

def adminEdit(request):
    return render(request, 'admin/adminEdit.html')

# Operator Edit lists
def list_operator(request):
    return render(request, 'lists/list_operator.html')

def list_services(request):
    if request.method == "POST":
        if request.POST.get("hair"):
            # hair bvrtgeh service duudna
            return redirect("list_services")
    else:
        return render(request, 'lists/list_services.html')

def list_sales(request):
    return render(request, 'lists/list_sales.html')

def list_location(request):
    return render(request, 'lists/list_location.html')

def list_orderlist(request):
    orders = [
        {
            "order" : "Туяа",
            "phone" : 99554488,
            "date" : "2024/12/19 12:00:00",
        },
        {
            "order" : "Батаа",
            "phone" : 80528787,
            "date" : "2024/02/07 16:00:00",
        },
        {
            "order" : "Гэрлээ",
            "phone" : 99887799,
            "date" : "2024/06/01 14:00:00",
        },
    ]
    context = {
        "orders" : orders
    }
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
        
    print(context)
    return render(request, 'lists/order_details.html',context)

def list_workers(request):
    return render(request, 'lists/list_workers.html')

# Edit Pages
def edit_operator(request):
    return render(request, 'editPages/edit_operator.html')

def edit_services(request):
    return render(request, 'editPages/edit_services.html')

def edit_sales(request):
    return render(request, 'editPages/edit_sales.html')

def edit_location(request):
    return render(request, 'editPages/edit_location.html')

def edit_orderlist(request):
    return render(request, 'editPages/edit_orderlist.html')

def edit_workers(request):
    return render(request, 'editPages/edit_workers.html')

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
    return render(request, 'operator/operator.html')

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
        con = requests.post(f"{BE_URL}/login/", data= json.dumps(jsons))
        result = json.loads(con.text)
        if result['resultCode'] == 200:
            return redirect("index")
        else:
            return render(request, 'signUp/login.html')
    else:
        return render(request, 'signUp/login.html')
    
def register(request):
    if request.method == "POST":
        jsons = {
            "action" : "login",
            "phone" : "",
            "password": "",
            "username" : "",
            "email": "",
        }
        jsons['password'] = request.POST.get('password') 
        jsons['phone'] = request.POST.get('phone')
        jsons['username'] = request.POST.get('username') 
        jsons['email'] = request.POST.get('email')
        con = requests.post(f"{BE_URL}/register/", data= json.dumps(jsons))
        result = json.loads(con.text)
        print(f"result: {result['resultCode']}")
        if result['resultCode'] == 200:
            return redirect("login")
        else:
            context = {'errorMessage' : result['resultMessege']}
            return render(request, 'signUp/register.html',context)
    else:
        return render(request, 'signUp/register.html')
    