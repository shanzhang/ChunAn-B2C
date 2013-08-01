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
from groupon.models import Groupon
import simplejson
import time
import models
from django.utils.timezone import utc

def groupon(request):
    return render_to_response("groupon/groupon.html",{'user':request.user,'cart':getCart(request.user.username)})

def getAllItem(request):
    date_time = time.strftime("%Y-%m-%d %X", time.localtime())
    if 'all' in request.GET:
        group = Groupon.objects.all()
    else:
        group = Groupon.objects.filter(begin_date__lte=date_time,end_date__gte=date_time)
    count = 0
    if group is None:
        return HttpResponse(simplejson.dumps({'count':count}))
    data = {}
    groupItem = []
    for ob in group:
        if ob is not None:
            groupItem.append({'gid':ob.id,'gpid':ob.gpid,'name':ob.name,'amount':ob.amount,'price':ob.price,'net_price':ob.net_price,'description':ob.description,'begin_date':str(ob.begin_date),'end_date':str(ob.end_date),'image':ob.image,'sell_amount':ob.sell_amount})
            count = count + 1
    data['count'] = count
    data['groupItem'] = groupItem
    data = simplejson.dumps(data)
    return HttpResponse(data)

def buyGrouponItem(request, offset):
    return HttpResponse()

def insertItem(gpid, name, amount, price, net_price, description, begin_date, end_date, image):
    group = Groupon()
    group.gpid = int(gpid) * (-1)
    group.name = name
    group.amount = amount
    group.sell_amount = 0
    group.price = price
    group.net_price = net_price
    group.description = description
    group.begin_date = begin_date
    group.end_date = end_date
    group.image = image
    group.save()
    return 1

def delay_groupon(request):
    end_date = request.GET['end_date']
    gpid = request.GET['gpid']
    groupon = Groupon.objects.filter(gpid=gpid)
    groupon.end_date = end_date
    groupon.update()
    return HttpResponse(1)

def deleteItem(pid):
    item = Groupon.objects.get(gpid=pid)
    item.delete()
    return 1

def modifyItem(gpid, name, amount, price, net_price, description, begin_date, end_date, image):
    group = Groupon()
    group.gpid = -gpid
    group.name = name
    group.amount = amount
    group.price = price
    group.net_price = net_price
    group.description = description
    group.begin_date = begin_date
    group.end_date = end_date
    group.image = image
    group.save()
    return 1

def payGroupon(request):
    gpid = request.GET['gpid']
    price = request.GET['price']
    shippingName = request.GET['shippingName']
    address = request.GET['address']
    city = request.GET['city']
    zipcode = request.GET['zip']
    phone = request.GET['phone']
    province = request.GET['province']
    amount = request.GET['amount']
    user_id = request.user.id
    gid = request.GET['gid']
    return HttpResponse(models.gPay(gpid,price,shippingName,address,city,zipcode,phone,province,amount,user_id,gid))