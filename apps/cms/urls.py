from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    path('index/', views.index_cms, name='index'),
    path('write_news/', views.WriteNewsView.as_view(), name='write_news'),
    path('category_news/', views.category_news, name='category_news'),
    path('add_category/', views.add_category, name='add_category'),
    path('edit_category/', views.edit_category, name='edit_category'),
    path('del_category/', views.del_category, name='del_category'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('news_manage/', views.NewsManage.as_view(), name='news_manage'),
    path('edit_news/', views.EditNewsView.as_view(), name='edit_news'),
    path('del_news/', views.del_news, name='del_news'),
    path('staff_manage/', views.StaffView.as_view(), name='staff_manage'),
    path('del_staff/', views.del_staff, name='del_staff'),
]
