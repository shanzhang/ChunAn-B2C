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

def detail_display(request,offset):
    data = models.detail_display(offset)
    return render_to_response("product/detail.html",{'data':data,'user':request.user,'cart':getCart(request.user.username)})

def loadCompare(request):
    return HttpResponse(models.loadCompare(request.GET['cate'],request.GET['myId']))

def loadNewOn(request):
    return HttpResponse(models.loadNewOn(request.GET['myId']))