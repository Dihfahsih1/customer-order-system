from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('customer/<str:pk>/', views.customer, name="customer"),
    path('products/', views.products, name="products"),
    path('create-order/', views.createOrder, name="create_order"),
    path('update-order/<str:pk>/', views.UpdateOrder, name="update_order"),
]
