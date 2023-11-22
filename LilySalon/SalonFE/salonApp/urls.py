from django.contrib import admin
from django.urls import path
from salonApp import views


urlpatterns = [
    # user page url
    path('', views.index, name = 'index'),
    path('services/', views.services, name = 'services'),
    path('order/', views.order, name = 'order'),

    path('adminEdit/', views.adminEdit, name = 'adminEdit'),
    path('a_location/', views.a_location, name = 'a_location'),

    # Lists
    path('list_services/', views.list_services, name = 'list_services'),
    path('list_operator/', views.list_operator, name = 'list_operator'),
    path('list_sales/', views.list_sales, name = 'list_sales'),
    path('list_location/', views.list_location, name = 'list_location'),
    path('list_orderlist/', views.list_orderlist, name = 'list_orderlist'),
    path('list_workers/', views.list_workers, name = 'list_workers'),

    # editPages url
    path('edit_services/', views.edit_services, name = 'edit_services'),
    path('edit_operator/', views.edit_operator, name = 'edit_operator'),
    path('edit_sales/', views.edit_sales, name = 'edit_sales'),
    path('edit_location/', views.edit_location, name = 'edit_location'),
    path('edit_orderlist/', views.edit_orderlist, name = 'edit_orderlist'),
    path('edit_worker/', views.edit_worker, name = 'edit_worker'),

    # addPages url
    path('add_services/', views.add_services, name = 'add_services'),
    path('add_operator/', views.add_operator, name = 'add_operator'),
    path('add_sales/', views.add_sales, name = 'add_sales'),
    path('add_location/', views.add_location, name = 'add_location'),
    path('add_orderlist/', views.add_orderlist, name = 'add_orderlist'),
    path('add_workers/', views.add_workers, name = 'add_workers'),
    

    # operator page url
    path('operator/', views.operator, name = 'operator'),


    # sign up
    path('login/', views.login, name = 'login'),
    path('register/', views.register, name = 'register'),
]
