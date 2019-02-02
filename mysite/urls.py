"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.news import views

urlpatterns = [
    path('',views.index_view, name='index'),
    path('news/', include('apps.news.urls')),
    path('auth/', include('apps.login.urls')),
    path('cms/', include('apps.cms.urls')),
    path('ueditor/', include('apps.ueditor.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# 添加MEDIA_ROOT下的访问路径
