# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db import connection
from django.template import RequestContext
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from groupon.views import insertItem
import models

@login_required
def admin_display(request):
    if 'is_superuser' in request.session and request.session['is_superuser'] == True:
        return render_to_response("admin/admin.html",{'user':request.user})

@login_required
def add_category(request):
    if 'is_superuser' in request.session and request.session['is_superuser'] == True:
        return render_to_response("admin/category_a.html",{'user':request.user})

@login_required
def del_category(request):
    if 'is_superuser' in request.session and request.session['is_superuser'] == True:
        return render_to_response("admin/category_d.html",{'user':request.user})

@login_required
def mod_category(request):
    if 'is_superuser' in request.session and request.session['is_superuser'] == True:
        return render_to_response("admin/category_m.html",{'user':request.user})

@login_required
def add_product(request):
    if 'is_superuser' in request.session and request.session['is_superuser'] == True:
        return render_to_response("admin/product_a.html",{'user':request.user})

@login_required
def del_product(request):
    if 'is_superuser' in request.session and request.session['is_superuser'] == True:
        return render_to_response("admin/product_d.html",{'user':request.user})

@login_required
def mod_product(request):
    if 'is_superuser' in request.session and request.session['is_superuser'] == True:
        if 'product_id' in request.GET:
            pid = request.GET['product_id']
        else:
            pid = 0
        if 'cid' in request.GET:
            cid = request.GET['cid']
        else:
            cid = 0
        if 'name' in request.GET:
            name = request.GET['name']
        else:
            name = 0
        if 'cname' in request.GET:
            cname = request.GET['cname']
        else:
            cname = 0
        return render_to_response("admin/product_m.html",{'user':request.user,'pid':pid,'cid':cid,'name':name,'cname':cname})

@login_required
def add_groupon(request):
    if 'is_superuser' in request.session and request.session['is_superuser'] == True:
        return render_to_response("admin/groupon_a.html",{'user':request.user})

@login_required
def del_groupon(request):
    if 'is_superuser' in request.session and request.session['is_superuser'] == True:
        return render_to_response("admin/groupon_d.html",{'user':request.user})

@login_required
def mod_groupon(request):
    if 'is_superuser' in request.session and request.session['is_superuser'] == True:
        return render_to_response("admin/groupon_m.html",{'user':request.user})

@login_required
def addGroupon(request):
    if 'is_superuser' in request.session and request.session['is_superuser'] == True:
        gpid = request.GET['gpid']
        name = request.GET['name']
        amount = request.GET['amount']
        price = request.GET['price']
        net_price = request.GET['gprice']
        description = request.GET['desc']
        begin_date = request.GET['begin_date']
        end_date = request.GET['end_date']
        image = request.GET['image']
        return HttpResponse(insertItem(gpid, name, amount, price, net_price, description, begin_date, end_date, image))

@login_required
def loadCategory(request):
    return HttpResponse(models.getCategory())

@login_required
def addCategory(request):
    parent = request.GET['parent']
    son = request.GET['son']
    models.addCategory(parent,son)
    return HttpResponse(1)

@login_required
def deleteCategory(request):
    cid = request.GET['cid']
    return HttpResponse(models.deleteCategory(cid))

@login_required
def modifyCategory(request):
    parent = request.GET['parent']
    cur_cate = request.GET['cur_cate']
    son = request.GET['son']
    models.modifyCategory(parent,cur_cate,son)
    return HttpResponse(1)

@login_required
def loadLeafCategory(request):
    return HttpResponse(models.loadLeafCategory())

@login_required
def addProduct(request):
    cate = request.GET['cate']
    name = request.GET['name']
    price = request.GET['price']
    desc = request.GET['desc']
    keywords = request.GET['keywords']
    title = request.GET['title']
    active = request.GET['active']
    amount = request.GET['amount']
    image = request.GET['image']
    models.addProduct(cate,name,price,desc,keywords,title,active,amount,image)
    return HttpResponse(1)

@login_required
def loadProduct(request):
    cate = request.GET['cate']
    return HttpResponse(models.loadProduct(cate))

@login_required
def loadProductInfo(request):
    pid = request.GET['pid']
    return HttpResponse(models.loadProductInfo(pid))

@login_required
def deleteProduct(request):
    product_id = request.GET['product_id']
    models.deleteProduct(product_id)
    return HttpResponse(1)

@login_required
def modifyProduct(request):
    product_id = request.GET['product_id']
    cate = request.GET['cate']
    name = request.GET['name']
    price = request.GET['price']
    desc = request.GET['desc']
    keywords = request.GET['keywords']
    title = request.GET['title']
    active = request.GET['active']
    amount = request.GET['amount']
    image = request.GET['image']
    models.modifyProduct(product_id,cate,name,price,desc,keywords,title,active,amount,image)
    return HttpResponse(1)

def search_product(request):
    query = request.GET['query']
    return HttpResponse(models.search_product(query))

def process_order(request):
    if 'is_superuser' in request.session and request.session['is_superuser'] == True:
        return render_to_response('admin/order_process.html',{'user':request.user})

def dp_groupon(request):
    if 'is_superuser' in request.session and request.session['is_superuser'] == True:
        return render_to_response('admin/dp_groupon.html',{'user':request.user})

def add_pure_groupon(request):
    if 'is_superuser' in request.session and request.session['is_superuser'] == True:
        return render_to_response('admin/pure_groupon.html',{'user':request.user})

def search_order(request):
    if 'is_superuser' in request.session and request.session['is_superuser'] == True:
        return render_to_response('admin/order_search.html',{'user':request.user})

def loadOrderAdmin(request):
    return HttpResponse(models.loadOrderAdmin())

def sendProduct(request):
    oid = request.GET['oid']
    return HttpResponse(models.sendProduct(oid))

def searchOrderAdmin(request):
    query = request.GET['query']
    search_type = request.GET['type']
    start = request.GET['start'] + ':00'
    end = request.GET['end'] + ':00'
    return HttpResponse(models.searchOrderAdmin(query,search_type,start,end))

@login_required
def manageUser(request):
    return render_to_response("admin/customer_m.html",{'user':request.user})

@login_required
def searchUser(request):
    types = request.GET['types']
    keywords = request.GET['keywords']
    return HttpResponse(models.getUser(types,keywords))

@login_required
def activateUser(request):
    uid = request.GET['id']
    is_active = request.GET['is_active']
    return HttpResponse(models.activateUser(uid,is_active))

@login_required
def adminUser(request):
    uid = request.GET['id']
    admin_is_active = request.GET['admin_is_active']
    return HttpResponse(models.adminUser(uid,admin_is_active))

@login_required
def loadAllOrderAdmin(request):
    return HttpResponse(models.loadAllOrderAdmin())