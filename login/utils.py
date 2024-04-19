import hashlib

from login.models import ConfirmString


def hash_code(s, salt='mysite'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode()) # update方法只接收bytes类型
    return h.hexdigest()

from django.utils import timezone
import uuid

def make_confirm_string(user):
    code = str(uuid.uuid4())  # Generate a unique UUID
    ConfirmString.objects.create(code=code, user=user, create_time=timezone.now())
    return code

from django.core.mail import send_mail
from django.conf import settings

def send_email(email, code):
    subject = '请确认你的电子邮件地址'
    text_content = '''感谢注册，如果你看到这条消息，你的电子邮件服务器不提供HTML链接功能，请联系管理员！'''
    html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>www.yourwebsite.com</a>，\
                    这只是一个测试站点，真正的站点名称将会在正式运行时告知，\
                    请点击站点链接完成注册确认！\
                    此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)
    send_mail(subject, text_content, settings.EMAIL_HOST_USER, [email], fail_silently=False, html_message=html_content)