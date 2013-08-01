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
from django.utils import simplejson

def addAddress(request):
    addName = request.GET['addName']
    addAdetail = request.GET['addAdetail']
    addCity = request.GET['addCity']
    addProvince = request.GET['addProvince']
    addPhone = request.GET['addPhone']
    zipcode = request.GET['zipcode']
    user_id = request.user.id
    ab = models.AddressBook()
    ab.insertAddress(user_id, addName, addAdetail, zipcode, addCity, addProvince, addPhone)
    return HttpResponse(1)

def loadAddressBook(request):
    ab = models.AddressBook()
    re = ab.getAddressBook(request.user.id)
    if re is None:
        return HttpResponse(simplejson.dumps({'count':0}))
    count = 0
    data = {}
    book = []
    for ob in re:
        if ob is not None:
            book.append({'id':ob.id,'receiver':ob.receiver_name,'address':ob.address_line_1,'zipcode':ob.zip_code,'city':ob.city,'province':ob.province,'phone':ob.phone})
            count = count +1
    data['count'] = count
    data['book'] = book
    data = simplejson.dumps(data)
    return HttpResponse(data)

def modAddress(request):
    aid = request.GET['aid']
    addName = request.GET['addName']
    addAdetail = request.GET['addAdetail']
    addCity = request.GET['addCity']
    addProvince = request.GET['addProvince']
    addPhone = request.GET['addPhone']
    zipcode = request.GET['zipcode']
    user_id = request.user.id
    ab = models.AddressBook()
    ab.updateAddress(aid, user_id, addName, addAdetail, zipcode, addCity, addProvince, addPhone)
    return HttpResponse(1)

def delAddress(request):
    aid = request.GET['aid']
    user_id = request.user.id
    ab = models.AddressBook()
    ab.deleteAddress(aid, user_id)
    return HttpResponse(1)