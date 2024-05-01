from django.db import models

class SiteUser(models.Model):
    Usertype = (
        ('1', "科研工作者"),
        ('2', "审核者"),
        ('3', "企业"),
    )
    name = models.CharField(max_length=128, unique=True, verbose_name="用户名")
    password = models.CharField(max_length=256, verbose_name="密码")
    email = models.EmailField(unique=True, verbose_name="电子邮箱")
    usertype = models.CharField(max_length=2, choices=Usertype, default='1', verbose_name="用户类型")
    organization = models.CharField(max_length=128, verbose_name="所属机构")
    department = models.CharField(max_length=128, verbose_name="所属部门")
    balance = models.IntegerField(default=100000, verbose_name="账户余额")
    # auto_now_add=True时为添加时的时间，更新对象时不会有变动。
    # auto_now=True无论是你添加还是修改对象，时间为你添加或者修改的时间。
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    modify_time = models.DateTimeField(auto_now=True, verbose_name="最后一次修改时间")
    # null针对数据库层面的， blank针对表单的
    last_login_time = models.DateTimeField(null=True, blank=True, verbose_name="最后一次登录时间")
    has_confirmed = models.BooleanField(default=False, verbose_name="是否邮箱验证")

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = "网站用户管理"
        verbose_name_plural = verbose_name


class ConfirmString(models.Model):
    code = models.CharField(max_length=256, verbose_name="确认码")
    user = models.OneToOneField('SiteUser', on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.user.name + ":" + self.code

    class Meta:
        ordering = ["-create_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"

