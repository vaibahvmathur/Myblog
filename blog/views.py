from django.shortcuts import render
import datetime


# Create your views here.
def HomePage(request):
    return render(request, 'blog_data.html', dict(Admin='vaibhav', time=datetime.datetime.now(), comment_count=str(0) + ' comment'))
