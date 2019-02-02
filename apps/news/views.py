from django.shortcuts import render, redirect
from django.conf import settings
from apps.cms.models import News
from apps.news.decorator import comment_login_required
from .serializers import NewsSerializer, CommentSerializer
from utils import restful
from django.http import Http404
from apps.news.forms import CommentForm
from apps.news.models import Comment


def index_view(request):
    count = settings.ONE_PAGE_NEWS_COUNT
    # select_related('author', 'category') 意思是提取将News模型中的外键字段查询出来，免得前端代码中再重新查找，这样得到了优化性能
    newses = News.objects.select_related('author', 'category').all()[0:count]
    context = {
        'newses': newses
    }
    return render(request, 'index/index.html', context=context)


def basket_news_view(request):
    newses = News.objects.select_related('author', 'category').filter(category_id=13)
    context = {
        'newses': newses
    }
    return render(request, 'basketball/basketball.html', context=context)


def autocar_news_view(request):
    newses = News.objects.select_related('author', 'category').filter(category_id=14)
    context = {
        'newses': newses
    }
    return render(request, 'autocar/autocar.html', context=context)


# 专门用来处理加载新闻的视图函数
def news_list(request):
    page = int(request.GET.get('p', 1))  # 后面1的意思是如果没有P默认p=1
    # get拿到的是一个字符串，需要转变为整数
    # 设定一个参数来获取当前新闻列表在哪一页
    # p参数的值是通过查询字符串的方式传过来的 news_list/?p=几,是js文件中传过来的。
    start = (page - 1) * settings.ONE_PAGE_NEWS_COUNT
    end = start + settings.ONE_PAGE_NEWS_COUNT
    # 这三行代码的意思就是定义当加载新闻列表时，显示的新闻数目，
    # 第一页默认显示2条，第二页则加载第三条跟第四天新闻。
    #  0，1  第一页 所有新闻可以看作是放在一个列表中，使用下标将其遍历出来
    #  2，3  第二页
    #  4，5  第三页
    newses = News.objects.select_related('author', 'category').all()[start:end]
    #  使用序列化将新闻列表加载出来。这里要记住。 REST framework django第三方插件
    #  将newes传进序列化函数中，因为newses是一个queryset，需要定义many
    seriailzer = NewsSerializer(newses, many=True)  # many=True代表newses中有很多字段
    data = seriailzer.data  # 将其中序列化后的值拿出来
    return restful.result(data=data)


def news_detail(request, news_id):
    try:  # try一下是因为get请求时，news_id能看到，如果用户直接将news_id改为一个数据库中没有的，将会报错
        # select_related('author', 'category') 意思是提取将News模型中的外键字段查询出来，免得前端代码中再重新查找，这样得到了优化性能
        # 但是当加载页面时，还是会请求数据库，查找评论的用户。这样查询次数多，性能不佳。
        # Comment定义的字段有News的外键
        # News模型prefetch_related通过Comment模型上的relate_name定义的comments得到当前News实列对应的Comment的所有字段，
        # 这里"comments__comment_author"是查找到所有评论的作者。个人理解，不知对不对，留待查资料。
        news = News.objects.select_related('author', 'category').prefetch_related("comments__comment_author").get(id=news_id)
        context = {
            'news': news
        }
        return render(request, 'news/news_detail.html', context=context)
    except News.DoesNotExist:  # 如果新闻不存在
        raise Http404


@comment_login_required
def comment_view(request):
    form = CommentForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data.get('content')  # 提取新闻内容
        news_id = form.cleaned_data.get('news_id')  # 提取新闻id
        try:
            news = News.objects.get(id=news_id)  # 根据新闻id获取新闻
            # 保存评论
            comment = Comment.objects.create(comment_content=content, comment_author=request.user, comment_news=news)
            # 使用arttemplate模板将评论显示出来，需要将数据序列化成json格式，那么定义一个序列化模型
            seriailzer = CommentSerializer(comment)  # 这里comment是一个Comment的对象
            data = seriailzer.data
            return restful.result(data=data)
        except News.DoesNotExist:
            raise Http404
    else:
        return restful.params_error(message=form.get_errors())



