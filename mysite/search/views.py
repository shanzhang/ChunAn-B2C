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

def search(request):
    query = request.GET['query']
    return render_to_response("search/search_result.html",{'user':request.user,'cart':getCart(request.user.username),'query':query})

def searchResult(request):
    return HttpResponse(models.search(request.GET['query']))