from rest_framework import serializers
from apps.cms.models import News,AddCategory
from apps.login.models import User
from apps.news.models import Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AddCategory
        fields = ('id', 'name')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('telephone', 'username', 'uuid', 'is_active', 'is_staff')


# 跟form表单类ModelForm使用方式很相似
# author category 再News模型中保存的是id ，需要重新序列化
class NewsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    author = UserSerializer()

    class Meta:
        model = News
        fields = ('id', 'title', 'thumbnail', 'desc', 'author', 'category', 'pub_time')


# 评论功能序列化
class CommentSerializer(serializers.ModelSerializer):
    comment_author = UserSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'comment_content', 'pub_time', 'comment_author')
