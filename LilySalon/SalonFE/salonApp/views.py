from django.shortcuts import render, redirect
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



def edit_operator(request):
    return render(request, 'editPages/edit_operator.html')

def edit_services(request):
    return render(request, 'editPages/edit_services.html')

def a_location(request):
    return render(request, 'admin/a_location.html')

def operator(request):
    return render(request, 'operator/operator.html')

def salesEdit(request):
    return render(request, 'operator/salesEdit.html')

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
    