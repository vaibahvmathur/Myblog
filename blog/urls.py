"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from blog.views import *
urlpatterns = [
    url(r'^$', HomePage, name='Homepage'),
    url(r'^registerpage/Register', Register, name='Register'),
    url(r'^registerpage/blog', redirectTohome, name='redirectTohome'),
    url(r'^registerpage/check_avail', check_avail, name='check_avail'),
    url(r'^registerpage/', registerpage, name='registerpage'),
    url(r'^mysore/', mysore, name='mysore')
]
