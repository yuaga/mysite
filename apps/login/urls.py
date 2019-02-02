from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('img_captcha/', views.img_captcha_view, name='img_captcha'),

]