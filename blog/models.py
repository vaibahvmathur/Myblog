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


def get_image_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.blogger.user.username, filename)


class BlogData(CommonInfo):
    blogger = models.ForeignKey(UserDetail, default=None)
    title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.FileField(upload_to=get_image_path)
    content_url = models.CharField(max_length=100)