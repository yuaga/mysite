from django.shortcuts import redirect
from utils import restful


# 定义一个装饰器，用来限制未登录用户评论。
def comment_login_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:  # 如果用户通过授权，就执行fuc函数,is_authenticated不能加括号，不然会保错
            return func(request, *args, **kwargs)
        else:
            if request.is_ajax():  # 如果是通过ajax请求，则弹出消息框提醒登录，js代码中有代码处理 window.messageBox.showError
                return restful.unauth(message='没有登录不能评论呀！~~')
            else:
                return redirect('/')
    return wrapper  # 记住这里不带括号


