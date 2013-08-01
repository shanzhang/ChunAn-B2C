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
from django.contrib.sessions.models import Session

def market(request):
    if 'is_superuser' in request.session and request.session['is_superuser'] == True:
        return render_to_response("admin/admin.html",{'user':request.user})
    else:
        return render_to_response("market/market.html",{'user':request.user,'cart':getCart(request.user.username)})

def market_display(request):
    return HttpResponse(models.market_display())

def terms(request):
    return render_to_response('terms.html')