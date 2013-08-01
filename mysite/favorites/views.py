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

def favorites(request):
    return render_to_response("favorites/favorites.html",{'user':request.user,'cart':getCart(request.user.username),'delFav':models.getFav(request.user.id)})

def addToFav(request,offset):
    pid = offset
    models.addToFav(request.user.id,pid)
    return HttpResponse(1)

def loadFav(request):
    return HttpResponse(models.loadFav(request.user.id))

def delFav(request):
    models.delFav(request.user.id)
    return render_to_response("favorites/favorites.html",{'user':request.user,'cart':getCart(request.user.username),'delFav':1})

def delFavItem(request,offset):
    return render_to_response("favorites/favorites.html",{'user':request.user,'cart':getCart(request.user.username),'delFav':models.delFavItem(request.user.id,offset)})

def updateFavItem(request):
    pid = request.GET['pid']
    models.updateFavItem(request.user.id,pid,amount)
    return HttpResponse(1)