from django.db import models
from apps.login.models import User
from apps.cms.models import News


class Comment(models.Model):
    comment_content = models.TextField()  # 评论内容
    pub_time = models.DateTimeField(auto_now_add=True)  # 发布时间
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)  # 发布者
    comment_news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')  # 评论所属的新闻
