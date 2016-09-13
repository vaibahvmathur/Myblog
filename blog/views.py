import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from models import *
import json
from django.core.exceptions import *

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
                    first_name=Name
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

