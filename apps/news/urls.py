from . import views
from django.urls import path

app_name = 'news'

urlpatterns = [
    path('news_list/', views.news_list, name='news_list'),
    path('<int:news_id>/', views.news_detail, name='news_detail'),
    path('basketball_news/', views.basket_news_view, name='basketball_news'),
    path('autocar_news/', views.autocar_news_view, name='autocar_news'),
    path('comment/', views.comment_view, name='comment'),
]
