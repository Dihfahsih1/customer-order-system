from django.shortcuts import render, redirect 
from django.http import HttpResponse
from .models import *
from .forms import *
from django.forms import inlineformset_factory


def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_orders = orders.count()
    total_customers=customers.count()
    total_delivered = orders.filter(status="Delivered").count()
    total_pending= orders.filter(status="Pending").count()
    context = {'orders':orders, 'customers':customers, 'total_orders':total_orders, 'total_customers':total_customers
    ,'total_delivered':total_delivered, 'total_pending':total_pending}
    return render(request,'accounts/dashboard.html', context)

def customer(request,pk):
    customer=Customer.objects.get(id=pk)
    orders=customer.order_set.all()
    total_orders = orders.count()
    context={'customer':customer,'orders':orders, 'total_orders':total_orders}
    return render(request,'accounts/customer.html', context)

def products(request):
    products = Product.objects.all()
    context={'products':products}
    return render(request,'accounts/products.html',context)
   
def createOrder(request, pk):
    customer=Customer.objects.get(id=pk)
    form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form, 'customer':customer }
    return render(request,'accounts/order_form.html',context)

def UpdateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form }
    return render(request,'accounts/order_form.html',context)

def DeleteOrder(request,pk):
    item = Order.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('/')
    context = {'item':item}
    return render(request, 'accounts/delete.html', context)