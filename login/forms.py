from captcha.fields import CaptchaField
from django import forms

from login.models import SiteUser


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', required=True,
                               min_length=4, max_length=128)
    password = forms.CharField(label="密码", required=True,
                               min_length=4, max_length=10)
    captcha = CaptchaField(label="验证码")


class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", required=True, max_length=128)
    password1 = forms.CharField(label="密码", max_length=256, required=True)
    password2 = forms.CharField(label="确认密码", max_length=256, required=True)
    email = forms.EmailField(label="邮箱地址")
    usertype = forms.ChoiceField(choices=SiteUser.Usertype, label="用户类型")
    organization = forms.CharField(label="所属机构", max_length=128)
    department = forms.CharField(label="所属部门", max_length=128)
    captcha = CaptchaField(label='验证码')

