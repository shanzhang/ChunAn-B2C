# Create your views here.
from django.db import models
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from cart.models import getCart
import models

@login_required
def order_display(request):
    return render_to_response("order/order.html",{'user':request.user,'cart':getCart(request.user.username)})

def loadOrder(request):
    return render_to_response("order/order_display.html",{'user':request.user,'cart':getCart(request.user.username)})

def loadOrderList(request):
    return HttpResponse(models.loadOrderList(request.user.username))

def payPass(request):
    password = request.GET['password']
    user = authenticate(username=request.user.username, password=password)
    if user is not None:
        return HttpResponse(1)
    else:
        return HttpResponse(0)

def pay(request):
    price1 = request.GET['price1']
    price2 = request.GET['price2']
    invoiceTag = request.GET['invoiceTag']
    invoiceCompany = request.GET['invoiceCompany']
    shippingName = request.GET['shippingName']
    address = request.GET['address']
    city = request.GET['city']
    zipcode = request.GET['zip']
    phone = request.GET['phone']
    message = request.GET['message']
    province = request.GET['province']
    return HttpResponse(models.pay(request.user.username,price1,price2,invoiceTag,invoiceCompany,shippingName,address,city,zipcode,phone,message,province))

def receiveProduct(request):
    oid = request.GET['oid']
    return HttpResponse(models.receiveProduct(oid))