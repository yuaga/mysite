from io import BytesIO
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from utils import restful
from utils.captcha.imgcapacha import Captcha
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
User = get_user_model()


def login_view(request):
    if request.method == 'GET':
        return render(request, 'login/login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data['telephone']
            password = form.cleaned_data['password']
            remember = form.cleaned_data['remember']
            user = authenticate(request, username=telephone, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    if remember:
                        request.session.set_expiry(None)
                    else:
                        request.session.set_expiry(0)
                        return redirect(reverse('index'))
                else:
                    message = '你的账号可能已经被拉黑了，快去重新注册一个吧！'
                    return render(request, 'login/login.html', locals())
            else:
                message = '手机号或者密码错误，重写填写吧！'
                return render(request, 'login/login.html', locals())
        else:
            message = form.get_errors()
            # message = '请正确填写手机号码或者密码'
            return render(request, 'login/login.html', locals())


def logout_view(request):
    logout(request)
    # return redirect('/index/')
    return redirect(reverse('index'))  # 注意这个方式


def register_view(request):
    if request.method == 'GET':
        return render(request, 'register/register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data['telephone']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            username = form.cleaned_data['username']
            img_captcha = form.cleaned_data['img_captcha']
            cache_img_captcha = cache.get(img_captcha.lower())
            # print(cache_img_captcha)
            # print('1')
            ex_user = User.objects.filter(telephone=telephone).exists()
            if not ex_user:
                if password1 == password2:
                    if cache_img_captcha == img_captcha.lower():
                        print(cache_img_captcha.lower())
                        user = User.objects.create_user(telephone=telephone, password=password1, username=username)
                        login(request, user)
                        return redirect(reverse('index'))
                    else:
                        message = '验证码输入错误！'
                        return render(request, 'register/register.html', locals())
                else:
                    message = '两次输入的密码不一致！'
                    return render(request, 'register/register.html', locals())
            else:
                message = '你的手机号码已被注册！'
                return render(request, 'register/register.html', locals())

        else:
            message = form.get_errors()
            return render(request, 'register/register.html', locals())


# def register_view(request):
#     if request.method == 'GET':
#         return render(request, 'register/register.html')
#     else:
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             telephone = form.cleaned_data.get('telephone')
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')
#             user = User.objects.create_user(telephone=telephone,username=username,password=password)
#             login(request,user)
#             return restful.ok()
#         else:
#             print(form.get_errors())
#             return restful.params_error(message=form.get_errors())


def img_captcha_view(request):
    text, image = Captcha.gene_code()
    # image 不能直接放在response中返回，需要借助流
    out = BytesIO()
    image.save(out, 'png')  # 将image保存入out中，以png这个类型
    out.seek(0)  # 当文件写入后，指针会指向最后，将指针移到最前面

    # HttpRrsponse 默认存储格式位字符串，此处定义为png格式
    response = HttpResponse(content_type='iamge/png')
    # 再将图片从out中读取出来，保存到response上，read()方法会在指针指向的位置开始读
    response.write(out.read())
    # tell方法可以获取当前指针的位置，代表当前图片的大小
    response['Content-length'] = out.tell()
    #  以字典键值对的方式放入cache  text.lower(): text.lower() ,有效期 5*60秒
    cache.set(text.lower(), text.lower(), 5 * 60)
    return response
