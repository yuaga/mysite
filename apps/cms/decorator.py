from functools import wraps
from django.http import Http404


# 限制某些人直接通过你的url地址访问一些限制的页面。
def blog_super_decorator(viewfunc):
    @wraps(viewfunc)  # 保留viewfunc函数的参数信息
    def decorator(request, *args, **kwargs):
        if request.user.is_superuser:
            return viewfunc(request, *args, **kwargs)
        else:
            raise Http404()
    return decorator
