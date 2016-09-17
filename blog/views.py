import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from models import *
import json
# from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
import os
from django.core.files import File

@login_required()
def HomePage(request):
    return render_to_response(
            'blog_data.html',
            dict(
                    Admin='vaibhav',
                    time=datetime.datetime.now(),
                    comment_count=str(0)+'comment'
            )
    )


@csrf_exempt
def Register(request):
    if request.method == 'POST':
        Username = request.POST['Username']
        Password = request.POST['Password']
        Email = request.POST['Email']
        Name = request.POST['Name']
        try:
            User.objects.get(Username=Username)
            message = "already exist"
        # except MultiValueDictKeyError:
        #     message = "error"
        except:
            user = User.objects.create_user(
                    username=Username,
                    password=Password,
                    email=Email,
                    first_name=Name,
            )
            userdetail = UserDetail()
            userdetail.user = user
            userdetail.save()
            message = "success"
    else:
        message = "error"
    return HttpResponse(json.dumps(dict(resultmessage=message)), content_type='application/javascript')


@csrf_exempt
def check_avail(request):
    response_dict = {}
    if request.method == 'POST':
        try:
            User.objects.get(username__iexact=request.POST['username'])
            response_dict.update({'get_avail': "error"})
        except User.DoesNotExist:
            response_dict.update({'get_avail': "success"})
    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')


@csrf_exempt
def registerpage(request):
    return render_to_response('register.html', {})

@csrf_exempt
def redirectTohome(request):
    return HttpResponseRedirect('/home')

@csrf_exempt
def redirectTologin(request):
    return HttpResponseRedirect('/admin')

@csrf_exempt
def login_auth(request):
    user = authenticate(username=request.POST['uname'], password=request.POST['pwd'])
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/home')
    else:
        return HttpResponseRedirect('/home')

def logout_auth(requset):
    logout(requset)
    return HttpResponseRedirect('/home')

@csrf_exempt
def mysore(request):
    return render_to_response('blog_pages/vaibhav/mysore.html', {})

@login_required()
def addblog(request):
    return render_to_response('addblog.html', {})

@csrf_exempt
def saveblog(request):
    print request.POST
    if request.user.is_authenticated():
        title = request.POST['blog-title']
        description = request.POST['blog-description']
        image = request.FILES['blog-image']
        content = request.POST['blog-full-data']

        logged_user = request.user
        logged_user_name = logged_user.username
        blogger = UserDetail.objects.get(user=logged_user)

        today = (datetime.datetime.now()).strftime('%d-%m-%Y')
        extention = '.html'
        fileName = str(title) + '_' + today + extention
        filepath = settings.BLOG_CONTENTS + '/' + logged_user_name + '/' + fileName

    else:
        print "not authenticated"
    return

