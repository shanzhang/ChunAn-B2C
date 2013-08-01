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
import models

def cart_display(request):
    return render_to_response("cart/cart.html",{'user':request.user,'cart':models.getCart(request.user.username)})

def addToCart(request):
    username = request.user.username
    pid = request.GET['pid']
    amount = request.GET['amount']
    models.addToCart(username,pid,amount)
    return HttpResponse(1)

def loadCart(request):
    return HttpResponse(models.loadCart(request.user.username))

def delCart(request):
    models.delCart(request.user.username)
    return render_to_response("cart/cart.html",{'user':request.user,'cart':models.getCart(request.user.username)})

def delCartItem(request,offset):
    models.delCartItem(request.user.username,offset)
    return render_to_response("cart/cart.html",{'user':request.user,'cart':models.getCart(request.user.username)})

def updateCartItem(request):
    pid = request.GET['pid']
    amount = request.GET['amount']
    models.updateCartItem(request.user.username,pid,amount)
    return HttpResponse(1)