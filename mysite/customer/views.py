# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from models import getUserInfo
from django.contrib import contenttypes

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('home')

def verifyUser(request):
    if 'username' in request.POST:
        usern = request.POST['username']
    else:
        usern = ''
    if 'password' in request.POST:
        passw = request.POST['password']
    else:
        passw = ''
    user = authenticate(username=usern, password=passw)
    if user is not None:
        if not user.is_active:
            return render_to_response("customer/register.html",{'cart':0,'fail':2})
        else:
            auth.login(request, user)
            userInfo = getUserInfo(usern)
            request.session['is_superuser'] = userInfo[3]
            #print(request.session['is_superuser'])
    else:
        return render_to_response("customer/register.html",{'cart':0,'fail':1})
    if request.session['is_superuser'] == True:
        return HttpResponseRedirect('admin')
    else:
        return HttpResponseRedirect('home')

def register(request):
    return render_to_response("customer/register.html",{'cart':0})

def createUser(request):
    userName = request.REQUEST.get('username', None)
    userPass = request.REQUEST.get('password', None)
    userMail = request.REQUEST.get('email', None)
    # TODO: check if already existed
    if userName and userPass and userMail:
        try:
            User.objects.get(username=userName)
            return HttpResponse(0)
        except User.DoesNotExist:
            try:
                User.objects.get(email=userMail)
                return HttpResponse(0)
            except User.DoesNotExist:
                user = User.objects.create_user(userName,userMail,userPass)
                user = authenticate(username=userName, password=userPass)
                auth.login(request, user)
                return HttpResponse(1)
    else:
        return HttpResponse(2)

def account(request):
    return render_to_response('customer/account.html',{'user':request.user,'cart':0,'fail':2})

def account_admin(request):
    return render_to_response('customer/account_admin.html',{'user':request.user,'fail':2})

def changeInfo(request):
    uid = request.user.id;
    password = request.POST['password'];
    new_password = request.POST['new_password'];
    confirm_password = request.POST['confirm_password'];
    if(not request.user.check_password(password)):
        return render_to_response("customer/account.html",{'user':request.user,'cart':0,'fail':1})
    if(new_password!=confirm_password):
        return render_to_response("customer/account.html",{'user':request.user,'cart':0,'fail':1})
    u = User.objects.get(id__exact=uid)
    u.set_password(new_password)
    u.save()
    user = authenticate(username=u.username, password=new_password)
    if user is not None:
        auth.login(request, user)
    return render_to_response("customer/account.html",{'user':request.user,'cart':0,'fail':0})

def changeInfo_admin(request):
    uid = request.user.id;
    password = request.POST['password'];
    new_password = request.POST['new_password'];
    confirm_password = request.POST['confirm_password'];
    if(not request.user.check_password(password)):
        return render_to_response("customer/account_admin.html",{'user':request.user,'fail':1})
    if(new_password!=confirm_password):
        return render_to_response("customer/account_admin.html",{'user':request.user,'fail':1})
    u = User.objects.get(id__exact=uid)
    u.set_password(new_password)
    u.save()
    user = authenticate(username=u.username, password=new_password)
    if user is not None:
        auth.login(request, user)
    return render_to_response("customer/account_admin.html",{'user':request.user,'fail':0})