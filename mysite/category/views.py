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
from cart.models import getCart

def category_display(request):
    return render_to_response("category/category_main.html",{'user':request.user,'cart':getCart(request.user.username)})

def category_main(request):
    return HttpResponse(models.getCategory())

def category_product(request,offset):
    return HttpResponse(models.category_product(offset))

def loadAllProduct(request):
    return HttpResponse(models.loadAllProduct())