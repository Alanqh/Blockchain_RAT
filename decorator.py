from functools import wraps
from django.shortcuts import redirect

def login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.session.get('is_login', None):
            # 如果用户已经登录，直接执行原函数
            return func(request, *args, **kwargs)
        else:
            # 如果用户未登录，重定向到登录页面
            return redirect('/login/')
    return wrapper



