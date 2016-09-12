import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from models import *
import json


@login_required
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
        print request.POST
        return render_to_response(
                'blog_data.html',
                dict(
                        Admin='vaibhav',
                        time=datetime.datetime.now(),
                        comment_count=str(0)+'comment'
                )
        )
        form = UserDetail(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
    else:
        pass
    return render_to_response(
            'blog_data.html',
            dict(
                    Admin='vaibhav',
                    time=datetime.datetime.now(),
                    comment_count=str(0)+'comment'
            )
    )


@csrf_exempt
def check_avail(request):
    response_dict = {}
    print request.POST
    print request.POST['username']
    if request.method == 'POST':
        try:
            User.objects.get(username__iexact=request.POST['username'])
            response_dict.update({'get_avail': "error"})
        except User.DoesNotExist:
            response_dict.update({'get_avail': "success"})
    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')

