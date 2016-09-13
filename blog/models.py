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