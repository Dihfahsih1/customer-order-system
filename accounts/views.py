from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse('home')

def customer(request):
    return HttpResponse('customer')

def products(request):
    return HttpResponse('products')

