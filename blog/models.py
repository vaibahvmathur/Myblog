from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class CommonInfo(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserDetail(CommonInfo):
    # user_name = models.CharField(max_length=30,unique=True)
    # first_name = models.CharField(max_length=30)
    # last_name = models.CharField(max_length=30, blank=True)
    # email = models.EmailField(max_length=254)

    username = forms.CharField(
            widget=forms.TextInput(
                    attrs=dict(
                            required=True,
                            max_length=30
                    )),
            label=_("Username"))
    email = forms.EmailField(
            widget=forms.TextInput(
                    attrs=dict(
                            required=True,
                            max_length=30
                    )),
            label=_("Email address"))
    password1 = forms.CharField(
            widget=forms.PasswordInput(
                    attrs=dict(
                            required=True,
                            max_length=30,
                            render_value=False
                    )),
            label=_("Password"))
    password2 = forms.CharField(
            widget=forms.PasswordInput(
                    attrs=dict(
                            required=True,
                            max_length=30,
                            render_value=False
                    )),
            label=("Password (again)"))
    name = forms.CharField(
            widget=forms.TextInput(
                    attrs=dict(
                            required=True,
                            max_length=30
                    )),
            label=_("name"))

    def clean_username(self):
        try:
            User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data
