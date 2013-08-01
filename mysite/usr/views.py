
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
from usr.models import *
from django.contrib.sessions.models import Session
from django.http import Http404


def allUser(request):
    if 'is_superuser' in request.session and request.session['is_superuser'] == True:
        data=getAllUsers()
        print data[0]
        return render_to_response("usr/allUser.html",{'userInfo':data[0][5]})
    else:
        raise Http404 # Create your views here.
