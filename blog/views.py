import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from models import BlogData, UserDetail, User
import json
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.db import transaction
import os
import codecs
import shutil


StartBlock = "{% extends 'home.html' %}\n" \
             "{%load staticfiles%}\n" \
             "{% block content %}\n" \
             "<div class='col-md-12 well well-success help-block'>\n"

EndBlock = "\n{% include 'comments.html' %}\n</div>\n{% endblock %}"

path_blog = settings.BLOG_CONTENTS


# @login_required()
def HomePage(request):
    blog_data = []
    posts = BlogData.objects.filter(active=1)
    for post in posts:
        temp_data = {}
        temp_data.update(
                name=post.blogger.user.username,
                time=post.created_date,
                title=post.title,
                description=post.description,
                comment_count=str(post.blogger.post_count) + ' comment',
                cover_image_url=post.image_url,
                content_url=post.content_url,
                blog_id=post.id)
        try:
            if request.user.is_staff:
                can_edit = 1
            elif request.user.username == post.blogger.user.username:
                can_edit = 1
            else:
                can_edit = 0
        except:
            can_edit = 0
        try:
            temp = authenticate(username=request.user.username, password=request.user.password)
            not_logged = 0
            loggedname = request.user.username
        except:
            not_logged = 1
            loggedname = 'Guest'
        temp_data.update(can_edit=can_edit)
        blog_data.append(temp_data)
    return render_to_response(
            'blog_data.html', {
                'blog_data': blog_data,
                'not_logged': not_logged,
                'loggedname': loggedname
            })


@csrf_exempt
def Register(request):
    if request.method == 'POST':
        Username = request.POST['Username']
        Password = request.POST['Password']
        Email = request.POST['Email']
        Name = request.POST['Name']
        try:
            User.objects.get(Username=Username)
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



@csrf_exempt
def logout_auth(requset):
    logout(requset)
    return HttpResponseRedirect('/admin')


@login_required()
def addblog(request):
    try:
        loggedname = request.user.username
    except:
        loggedname = 'Guest'
    return render_to_response('addblog.html', {'loggedname': loggedname})


@login_required()
@csrf_exempt
@transaction.atomic
def saveblog(request):
    if request.user.is_authenticated():
        auth_point = transaction.savepoint()
        title = request.POST['blog-title']
        description = request.POST['blog-description']
        blog_content = str(request.POST['blog-full-data'])
        content = str(StartBlock) + str(blog_content) + str(EndBlock)
        try:
            image = request.FILES['blog-image']
        except:
            image = None

        logged_user = request.user
        logged_user_name = logged_user.username
        blogger = UserDetail.objects.get(user=logged_user)
        post_number = blogger.post_count + 1
        today = (datetime.datetime.now()).strftime('%d-%m-%Y')
        extention_content = '.html'
        file_name = str(title) + '_' + today + extention_content
        path_to_dir = str(logged_user_name) + '/' + str(post_number)

        path_to_post_number = "templates/blog_pages/" + path_to_dir
        path_to_user_blog = path_to_post_number + '/' + str(file_name)
        path_to_post_number_save = "blog_pages/" + path_to_dir
        path_to_user_blog_save = path_to_post_number_save + '/' + str(file_name)

        if not os.path.exists(path_to_post_number):
            os.makedirs(path_to_post_number)
        abs_path = os.path.join(os.path.dirname('__file__'), path_to_user_blog).replace("\\", '/')
        with open(abs_path, 'w') as destination:
            destination.write(content)
        destination.close()

        try:
            path_to_post_number = "static/blog_pages/" + path_to_dir
            path_to_user_blog_image = path_to_post_number + '/' + str(image.name)
            path_to_user_blog_image_save = path_to_post_number_save + '/' + str(image.name)
            if not os.path.exists(path_to_post_number):
                os.makedirs(path_to_post_number)
            abs_path = os.path.join(os.path.dirname('__file__'), path_to_user_blog_image).replace("\\", '/')
            with open(abs_path, 'wb') as destination:
                destination.write(image.read())
            destination.close()
        except:
            path_to_user_blog_image_save = None

        blogger.post_count = post_number
        blogger.save()
        this_post = BlogData()
        this_post.blogger = blogger
        this_post.title = title
        this_post.description = description
        this_post.content_url = path_to_user_blog_save
        this_post.image_url = path_to_user_blog_image_save
        this_post.post_number = post_number
        this_post.save()
    else:
        transaction.savepoint_rollback(auth_point)
    return HttpResponseRedirect('/home')


@login_required()
@csrf_exempt
@transaction.atomic
def editblog(request, id):
    if request.user.is_authenticated():
        auth_point = transaction.savepoint()
        title = request.POST['blog-title']
        description = request.POST['blog-description']
        blog_content = str(request.POST['blog-full-data'])
        content = str(StartBlock) + str(blog_content) + str(EndBlock)
        try:
            image = request.FILES['blog-image']
        except:
            image = None

        this_post = BlogData.objects.get(id=int(id))
        logged_user = this_post.blogger.user
        logged_user_name = logged_user.username
        post_number = this_post.post_number
        today = (datetime.datetime.now()).strftime('%d-%m-%Y')
        extention_content = '.html'
        file_name = str(title) + '_' + today + extention_content
        path_to_dir = str(logged_user_name) + '/' + str(post_number)

        path_to_post_number = "templates/blog_pages/" + path_to_dir
        path_to_user_blog = path_to_post_number + '/' + str(file_name)
        path_to_post_number_save = "blog_pages/" + path_to_dir
        path_to_user_blog_save = path_to_post_number_save + '/' + str(file_name)

        if os.path.exists(path_to_post_number):
            shutil.rmtree(path_to_post_number)
        os.makedirs(path_to_post_number)
        abs_path = os.path.join(os.path.dirname('__file__'), path_to_user_blog).replace("\\", '/')
        with open(abs_path, 'w') as destination:
            destination.write(content)
        destination.close()

        try:
            path_to_post_number = "static/blog_pages/" + path_to_dir
            path_to_user_blog_image = path_to_post_number + '/' + str(image.name)
            path_to_user_blog_image_save = path_to_post_number_save + '/' + str(image.name)
            if os.path.exists(path_to_post_number):
                shutil.rmtree(path_to_post_number)
            os.makedirs(path_to_post_number)
            abs_path = os.path.join(os.path.dirname('__file__'), path_to_user_blog_image).replace("\\", '/')
            with open(abs_path, 'wb') as destination:
                destination.write(image.read())
            destination.close()
            this_post.image_url = path_to_user_blog_image_save
        except:
            path_to_user_blog_image_save = None

        this_post.title = title
        this_post.description = description
        this_post.content_url = path_to_user_blog_save
        this_post.save()
    else:
        transaction.savepoint_rollback(auth_point)
    return HttpResponseRedirect('/home')


# @login_required()
@csrf_exempt
def getblog(request, post):
    try:
        blog = BlogData.objects.get(id=int(post))

    except BlogData.DoesNotExist:
        return HttpResponseRedirect('/home')
    try:
        temp = authenticate(username=request.user.username, password=request.user.password)
        not_logged = 0
        loggedname = request.user.username
    except:
        not_logged = 1
        loggedname = 'Guest'
    return render_to_response(blog.content_url, {'loggedname': loggedname,'not_logged': not_logged})


@login_required()
@csrf_exempt
def updateblog(request, post):
    try:
        blog = BlogData.objects.get(id=int(post))
        abs_path = os.path.join(os.path.dirname('__file__'), 'templates/'+blog.content_url).replace("\\", '/')
        contents = (codecs.open(abs_path, 'rb', encoding='utf-8')).readlines()[4:-2]
        content = ''
        for line in contents:
            content += str(line)

    except BlogData.DoesNotExist:
        return HttpResponseRedirect('/home')
    try:
        loggedname = request.user.username
    except:
        loggedname = "Guest"
    return render_to_response(
            'addblog.html',
            {
                'title': blog.title,
                'description': blog.description,
                'content': content,
                'update': 1,
                'id': blog.id,
                'loggedname': loggedname
            }
    )


@login_required()
@transaction.atomic
@csrf_exempt
def deleteblog(request):
    save_point = transaction.savepoint()
    response_dict = {}
    if request.method == 'POST':
        try:
            id = str(request.POST['id'])
            blog = BlogData.objects.get(id=int(id))
            user = blog.blogger
            post_count = int(user.post_count)
            logged_user = user.user
            logged_user_name = logged_user.username
            post_number = blog.post_number
            user.post_count -= 1
            user.save()
            blog.delete()
            path_to_dir = str(logged_user_name) + '/' + str(post_number)
            path_to_post_number = "templates/blog_pages/" + path_to_dir
            if os.path.exists(path_to_post_number):
                shutil.rmtree(path_to_post_number)
            response_dict.update({'message': "success"})
        except BlogData.DoesNotExist:
            transaction.savepoint_rollback(save_point)
            response_dict.update({'message': "error"})
    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
