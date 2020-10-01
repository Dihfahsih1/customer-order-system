from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('customer/<str:pk>/', views.customer, name="customer"),
    path('products/', views.products, name="products"),
    path('create-order/<str:pk>/', views.createOrder, name="create_order"),
    path('update-order/<str:pk>/', views.UpdateOrder, name="update_order"),
    path('delete-order/<str:pk>/', views.DeleteOrder, name="delete_order"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('user/', views.userPage, name="user-page"),
]
