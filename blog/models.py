from django.db import models
from django.contrib.auth.models import User


class CommonInfo(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserDetail(CommonInfo):
    user = models.ForeignKey(User, default=None)
    post_count = models.IntegerField(default=0)


class BlogData(CommonInfo):
    blogger = models.ForeignKey(UserDetail, default=None)
    title = models.CharField(max_length=50)
    description = models.TextField()
    content_url = models.CharField(max_length=100)
    image_url = models.CharField(max_length=100, blank=True, null=True, default=None)


def get_image_path(instance, filename):
    rel_path = 'templates/blog_pages/{0}/{1}/{2}'.format(instance.blogger.user.username, instance.blogger.post_count, filename)
    return rel_path
