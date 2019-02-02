from django import forms
from apps.forms import FormMixin
from django.contrib.auth import get_user_model
User = get_user_model()


class LoginForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11, min_length=11)
    password = forms.CharField(max_length=16, min_length=8)
    remember = forms.IntegerField(required=False)


class RegisterForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11, min_length=11)
    username = forms.CharField(max_length=10, min_length=1)
    password1 = forms.CharField(max_length=16, min_length=8)
    password2 = forms.CharField(max_length=16, min_length=8)
    img_captcha = forms.CharField(max_length=4, min_length=4)
