from django.contrib import admin
from django.urls import path
from salonApp import views


urlpatterns = [
    # user page url
    path('', views.index, name = 'index'),
    path('services/', views.services, name = 'services'),
    path('order/', views.order, name = 'order'),

    # operator page url
    path('adminEdit/', views.adminEdit, name = 'adminEdit'),
    path('a_admin/', views.a_admin, name = 'a_admin'),
    path('a_operator/', views.a_operator, name = 'a_operator'),
    path('a_location/', views.a_location, name = 'a_location'),

    # operator page url
    path('operatorEdit/', views.operatorEdit, name = 'operatorEdit'),
    path('salesEdit/', views.salesEdit, name = 'salesEdit'),

    # sign up
    path('login/', views.login, name = 'login'),
    path('register/', views.register, name = 'register'),
]
