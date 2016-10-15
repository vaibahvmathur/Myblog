"""My_Blog URL Configuration

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
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
import blog.views as blogview
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', blogview.redirectTologin, name='redirectTologin'),
    url(r'^home/', include('blog.urls')),
    # url(r'^Register', include('blog.urls')),
    url(r'^check_avail', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^registerpage/', include('blog.urls')),
    url(r'^admin/login', blogview.login_auth, name="login_auth"),
    url(r'^logout', blogview.logout_auth, name="logout_auth"),
    url(r'^addblog', blogview.addblog, name='addblog'),
    url(r'^saveblog', blogview.saveblog, name='saveblog'),
    url(r'blog/(?P<post>\d+)/$', blogview.getblog, name='get_blog'),
]
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)