from django.shortcuts import render, redirect 
from django.http import HttpResponse
from .models import *
from .forms import *
from django.forms import inlineformset_factory
from .filters import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group

@unauthenticated_user
def registerPage(request,instance):
    form = CreateUserForm()
    if request.method=='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,'Account was created succesfully for ' + username + ', you can now login')
            return redirect('login')
    context={'form':form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,'You have logged in successfully as ' + str(user) )
            return redirect('home')
        else:
            messages.info(request,'Username or password is incorrect')
    context={}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only  
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])     
def customer(request,pk):
    customer=Customer.objects.get(id=pk)
    orders=customer.order_set.all()
    total_orders = orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders=myFilter.qs
    context={'customer':customer,'orders':orders, 'total_orders':total_orders,'myFilter':myFilter}
    return render(request,'accounts/customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admins','customers'])     
def products(request):
    products = Product.objects.all()
    context={'products':products}
    return render(request,'accounts/products.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])        
def createOrder(request, pk):
    OrderFormSet= inlineformset_factory(Customer, Order, fields=('product','status'), extra=5)
    customer=Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    if request.method == 'POST':
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset':formset, 'customer':customer }
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])     
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])     
def DeleteOrder(request,pk):
    item = Order.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('/')
    context = {'item':item}
    return render(request, 'accounts/delete.html', context)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['customers'])   
def userPage(request):
    orders=request.user.customer.order_set.all()
    total_orders = orders.count()
    total_delivered = orders.filter(status="Delivered").count()
    total_pending= orders.filter(status="Pending").count()
    context={'orders':orders,'total_orders':total_orders,'total_delivered':total_delivered,'total_pending':total_pending}
    return render(request,'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customers'])     
def accountSettings(request):
    customer=request.user.customer
    form=customerForm(instance=customer)
    if request.method == 'POST':
        form=customerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your information has been updated')
            return redirect('user-account')

    context={'form':form}
    return render(request,'accounts/account_settings.html',context)
