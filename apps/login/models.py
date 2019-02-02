from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from shortuuidfield import ShortUUIDField


class UserManager(BaseUserManager):
    def _create_user(self, telephone, username, password, **kwargs):

        if not telephone:
            return ValueError('请输入手机号码')
        if not username:
            return ValueError('请输入用户名')
        if not password:
            return ValueError('请输入密码')
        #  下面固定写法，死记
        user = self.model(telephone=telephone, username=username, **kwargs)
        user.set_password(password)  # 设置密码
        user.save()
        return user

    def create_user(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(telephone=telephone, username=username, password=password, **kwargs)

    def create_superuser(self, telephone, username, password, **kwargs):

        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        # kwargs是一个字典结构，当前面加两个**时，系统会自动的将其分解成key=value的样式
        return self._create_user(telephone=telephone, username=username, password=password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    uuid = ShortUUIDField(primary_key=True)
    telephone = models.CharField(max_length=11, unique=True)
    username = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username
