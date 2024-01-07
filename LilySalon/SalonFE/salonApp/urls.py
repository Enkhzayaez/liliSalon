from django.contrib import admin
from django.urls import path
from salonApp import views


urlpatterns = [
    # user page url
    path('', views.index, name = 'index'),
    path('services/', views.services, name = 'services'),
    path('services/<int:occ_id>', views.services, name = 'services'),
    path('order/', views.order, name = 'order'),
    path('oremove_order_item/<int:item_id>', views.remove_order_item, name = 'remove_order_item'),
    path('order_confirm/', views.order_confirm, name = 'order_confirm'),
    path('order_confirm/<int:order_id>', views.order_confirm, name = 'order_confirm'),

    path('adminEdit/', views.adminEdit, name = 'adminEdit'),
    path('a_location/', views.a_location, name = 'a_location'),

    # Lists
    path('list_services/', views.list_services, name = 'list_services'),
    path('list_operator/', views.list_operator, name = 'list_operator'),
    path('list_sales/', views.list_sales, name = 'list_sales'),
    path('list_location/', views.list_location, name = 'list_location'),
    path('list_orderlist/', views.list_orderlist, name = 'list_orderlist'),
    path('list_workers/', views.list_workers, name = 'list_workers'),
    path('list_occupation/', views.list_occupation, name = 'list_occupation'),
    path('order_detail/<int:phone>', views.order_detail, name = 'order_detail'),

    # editPages url
    path('edit_operator/<int:operator_id>', views.edit_operator, name = 'edit_operator'),
    path('delete_operator/<int:operator_id>', views.delete_operator, name = 'delete_operator'),
    path('edit_sales/<int:sale_id>', views.edit_sales, name = 'edit_sales'),
    path('delete_sales/<int:sale_id>', views.delete_sales, name = 'delete_sales'),
    path('edit_location/<int:branch_id>', views.edit_location, name = 'edit_location'),
    path('delete_location/<int:branch_id>', views.delete_location, name = 'delete_location'),
    path('edit_order/<int:order_id>', views.edit_order, name = 'edit_order'),
    path('edit_workers/<int:worker_id>', views.edit_workers, name = 'edit_workers'),
    path('delete_workers/<int:worker_id>', views.delete_workers, name = 'delete_workers'),
    path('edit_occupation/<int:occupation_id>', views.edit_occupation, name = 'edit_occupation'),
    path('delete_occupation/<int:occupation_id>', views.delete_occupation, name = 'delete_occupation'),
    path('edit_service/<int:service_id>', views.edit_service, name = 'edit_service'),
    path('delete_service/<int:service_id>', views.delete_service, name = 'delete_service'),
    path('delete_order/<int:order_id>', views.delete_order, name = 'delete_order'),

    # addPages url
    path('add_services/', views.add_services, name = 'add_services'),
    path('add_operator/', views.add_operator, name = 'add_operator'),
    path('add_sales/', views.add_sales, name = 'add_sales'),
    path('add_location/', views.add_location, name = 'add_location'),
    path('add_orderlist/', views.add_orderlist, name = 'add_orderlist'),
    path('add_workers/', views.add_workers, name = 'add_workers'),
    

    # operator page url
    path('operator/', views.operator, name = 'operator'),

    path('refresh_order/', views.refresh_order, name = 'refresh_order'),


    # sign up
    path('login/', views.login, name = 'login'),
    path('logout/', views.logout, name='logout'),

    path('hairStyle/', views.hairStyle, name = 'hairStyle'),
]
