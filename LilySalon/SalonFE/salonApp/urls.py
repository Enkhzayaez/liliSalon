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
    path('edit_services/', views.edit_services, name = 'edit_services'),
    path('edit_operator/', views.edit_operator, name = 'edit_operator'),
    path('a_location/', views.a_location, name = 'a_location'),

    # operator page url
    path('operator/', views.operator, name = 'operator'),
    path('salesEdit/', views.salesEdit, name = 'salesEdit'),

    # sign up
    path('login/', views.login, name = 'login'),
    path('register/', views.register, name = 'register'),
]
