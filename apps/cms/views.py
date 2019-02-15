from django.contrib.auth.models import Group
from django.views.generic import View
from django.shortcuts import render, redirect, reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST, require_GET
from apps.cms.models import AddCategory, News
from utils import restful
from .forms import EditCategoryForm, EditNewsForm
import os
from django.conf import settings
from .forms import WriteNewsForm
from datetime import datetime
from django.utils.timezone import make_aware
from apps.login.models import User
from apps.cms.decorator import blog_super_decorator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required


# 如果不是公司员工，则不能进入下面的视图函数渲染的页面，CMS页面主页
@staff_member_required(login_url='index')
def index_cms(request):
    return render(request, 'cms/index.html')


# CMS发布新闻页面
# def write_news(request):
#     categories = AddCategory.objects.all()
#     context = {
#         'categories': categories
#     }
#     return render(request, 'cms/write_news.html', context=context)

# 将上面的代码改写，因为涉及到了新闻发布时需要POST请求，改为类视图
# 注意这个类视图的引用/from django.views.generic import View
# 类视图必须用method_decorator装饰器包裹起来，perm是权限的名称，login_url是没有权限要跳转的页面
@method_decorator(permission_required(perm='news.add_news', login_url='/'), name='dispatch')
class WriteNewsView(View):

    def get(self, request):
        categories = AddCategory.objects.all()
        context = {
            'categories': categories
        }
        return render(request, 'cms/write_news.html', context=context)

    # 接受发布新闻时用户输入的数据得使用POST方法，还要写一个models,映射数据库,写一个表单类，进行提取数据
    def post(self, request):
        form = WriteNewsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            category = form.cleaned_data.get('category')
            # category_id = form.cleaned_data.get('category')  # 这里实验了这两个方式，展示出来的结果是不是一样，结果是一样。
            # category = AddCategory.objects.get(pk=category_id)
            print(category)  # 实验上面两种代码，返回的结果都是一样的，都是AddCategory object (14)，即一个对象，还是需要前端代码中调用他的属性名
            # 所以依照代码越少的原则，使用只有一行代码的
            News.objects.create(title=title, desc=desc, thumbnail=thumbnail,
                                content=content, category=category, author=request.user)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


@method_decorator(permission_required(perm='news.change_news', login_url='/'), name='dispatch')
class EditNewsView(View):

    # 实现get请求后，可以将需要修改的数据拿到，修改完也可以提交，但是是新增一个文章了。这不是想要的，只是需要修改。
    def get(self, request):
        news_id = request.GET.get('news_id')
        news = News.objects.get(id=news_id)
        # print(type(news))
        context = {
            'news': news,
            'categories': AddCategory.objects.all()
        }
        return render(request, 'cms/write_news.html', context=context)

    # 修改新闻的视图函数写完了，当点击提交按钮时，如何判断这个新闻是不是修改的呢？可以再按键上绑定新闻的ID，如果有这个ID，说明是要修改的
    def post(self, request):
        form = EditNewsForm(request.POST)
        # print(121213)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            category = form.cleaned_data.get('category')
            pk = form.cleaned_data.get('id')
            News.objects.filter(id=pk).update(title=title, desc=desc, thumbnail=thumbnail, content=content,
                                              category=category)
            # print(121212)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


@require_POST
@permission_required(perm='news.change_news', login_url='/')
def del_news(request):
    news_id = request.POST.get('pk')
    News.objects.filter(pk=news_id).delete()
    return restful.ok()


# 新闻发布页面中的新闻分类页面
@require_GET
@permission_required(perm='news.change_addcategory', login_url='/')
def category_news(request):
    context = {
        'categories': AddCategory.objects.all()
    }
    return render(request, 'cms/category.html', context=context)


# 新闻分类页面中，增加新闻分类
@require_POST
@permission_required(perm='news.add_addcategory', login_url='/')
def add_category(request):
    name = request.POST.get('name')
    exists = AddCategory.objects.filter(name=name)
    if not exists:
        AddCategory.objects.create(name=name)
        return restful.ok()
    else:
        return restful.params_error(message='分类已存在~')


# 新闻分类页面中，修改新闻分类
@require_POST
@permission_required(perm='news.change_addcategory', login_url='/')
def edit_category(request):
    form = EditCategoryForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data['pk']
        name = form.cleaned_data['name']
        exists = AddCategory.objects.filter(name=name)
        if not exists:
            try:
                AddCategory.objects.filter(pk=pk).update(name=name)
                return restful.ok()
            except:
                return restful.params_error(message='分类不存在')
        else:
            return restful.params_error(message='分类已存在~')
    return restful.params_error(message='重新操作！')


# 新闻分类页面中，删除新闻分类
@require_POST
@permission_required(perm='news.delete_addcategory', login_url='/')
def del_category(request):
    pk = request.POST.get('pk')
    try:
        categories = AddCategory.objects.filter(pk=pk).delete()
        return restful.ok()
    except:
        return restful.params_error(message='分类不存在')


# 下面写的是新闻发布页面中，点击上传文件的视图函数。
@require_POST
@permission_required(perm='news.add_news', login_url='/')
def upload_file(request):
    file = request.FILES.get('file')  # 此处的get中的file是你要获取的文件的字段名，要跟前端保持一致。
    name = file.name  # 然后获取文件的名字。
    with open(os.path.join(settings.MEDIA_ROOT, name), 'wb') as uf:  # 此处是打开文件，以2进制的方式写入
        for chunk in file.chunks():  # chunks()函数是 读取文件并生成'chunk_size'字节块，所以要将其遍历出来，可以查看源码
            uf.write(chunk)  # 将读取出来的字节写入uf中，其实也就是上传
    url = request.build_absolute_uri(settings.MEDIA_URL + name)
    return restful.result(data={'url': url})


# 新闻管理中的查询视图函数
@method_decorator(permission_required(perm='news.add_news', login_url='/'), name='dispatch')
class NewsManage(View):

    def get(self, request):
        # 这里get得到的是字符串，需要转换为整数
        start = request.GET.get('start')
        end = request.GET.get('end')
        title = request.GET.get('title')
        # request.GET.get(参数)
        # 这个默认值是只有 这个参数没有传递时,得到的是一个NoneType，会报错
        # 那么就设置一个0，当参数没有值时，用0代替
        category_id = int(request.GET.get('category') or 0)
        newses = News.objects.select_related('author', 'category')

        if start or end:
            if start:
                start_date = datetime.strptime(start, '%Y/%m/%d')  # 将字符串时间格式化
            else:
                start_date = datetime(year=2019, month=1, day=1)  # 如果用户没有选择开始时间，则设置为2019/1/1
            if end:
                end_date = datetime.strptime(end, '%Y/%m/%d')
            else:
                end_date = datetime.now()
            # start_date, end_date 都是幼稚时间，pub_time是清醒时间，所以下面代码会报错
            # from django.utils.timezone import make_aware 调用这个方法可以将幼稚时间转为清醒时间
            # newses = newses.filter(pub_time__range=(start_date, end_date))  # 从开始时间，结束时间之间过滤
            newses = newses.filter(pub_time__range=(make_aware(start_date), make_aware(end_date)))  # 从开始时间，结束时间之间过滤
        if title:
            newses = newses.filter(title__icontains=title)  # 不区分大小写 ，包含的意思
            # print(title)
        if category_id:
            newses = newses.filter(category=category_id)
            # print(category_id)
        context = {
            'newses': newses,
            'categories': AddCategory.objects.all(),
            'title': title,
            'start': start,
            'end': end,
            'category_id': category_id

        }
        return render(request, 'cms/newsmanage.html', context=context)


# 类视图函数不能直接调用装饰器，需要借助@method_decorator()方法，method_decorator的作用是为函数视图装饰器补充第一个self参数，以适配类视图方法
# 装饰器需要的第一个参数是 request对象, 但我们调用类视图中请求方法时, 传入的第一个参数不是request对象，而是self 视图对象本身，第二个位置参数才是request对象
# 所以如果直接将用于函数视图的装饰器装饰类视图方法，会导致参数传递出现问题。
# 这么dispatch不知道什么意思，为类视图函数下面的所有方法添加装饰器
# @method_decorator 中添加name属性，可以为特定的方法添加装饰器，比如get ,post某个特定的
# 装饰器一些使用方法不懂的看博客
@method_decorator(blog_super_decorator, name='dispatch')
class StaffView(View):

    def get(self, request):
        staffs = User.objects.filter(is_staff=True)
        groups = Group.objects.all()
        context = {
            "staffs": staffs,
            'groups': groups
        }
        return render(request, 'cms/staffs.html', context=context)

    def post(self, request):
        telephone = request.POST.get('telephone')
        user = User.objects.filter(telephone=telephone).first()
        print(user)
        if user:
            user.is_staff = True
            group_id = request.POST.get('group')
            group = Group.objects.filter(id=group_id).first()
            # print(group)
            user.groups.add(group)
            user.save()
            return restful.ok()
        else:
            return restful.params_error(message='这个员工好像不存在呀！~')


@require_POST
@blog_super_decorator
def del_staff(request):
    telephone = request.POST.get('telephone')
    print(telephone)
    try:
        staff = User.objects.filter(telephone=telephone).delete()
        return restful.ok()
    except:
        return restful.params_error(message='员工不存在！')




