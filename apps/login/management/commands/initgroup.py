from django.core.management.base import BaseCommand  # 创建命令的基类
from django.contrib.auth.models import ContentType, Group, Permission
from apps.news.models import Comment
from apps.cms.models import AddCategory, News


# 创建一个命令，initgroup是一个初始化命令文件,初始化时，会找到Commands这个类，如果没有这个类就不行。
class Command(BaseCommand):
    def handle(self, *args, **options):
        # 先创建一个新闻编辑组，用来发布新闻，编辑新闻
        # 我们可以根据数据库中表的关系找到ContentType id与model的关系，找到id后可以将对应的权限找到
        # get_for_model,在这里的用处是可以通过模型找到content type
        edit_content_types = [
            ContentType.objects.get_for_model(News),
            ContentType.objects.get_for_model(AddCategory)
        ]
        # 接下来找到了content type id ，那么就根据这个id将权限找出来
        # content_type__in = edit_content_types 可以理解为content_type再edit_content_types中
        edit_permissions = Permission.objects.filter(content_type__in=edit_content_types)
        # 找到了content type 接下来是不是就要创建一个分组啊？将权限加到这个分组上
        editGroup = Group.objects.create(name='新闻编辑猿')
        editGroup.permissions.set(edit_permissions)  # 这样一个权限就创建好了
        editGroup.save()   # 这个保存不能忘了
        self.stdout.write(self.style.SUCCESS('新闻小编创建完成'))

        # 创建一个管理组，用来管理评论
        manage_content_types = [
            ContentType.objects.get_for_model(Comment)
        ]
        manage_permissions = Permission.objects.filter(content_type__in=manage_content_types)
        manageGroup = Group.objects.create(name='评论管理猿')
        manageGroup.permissions.set(manage_permissions)
        manageGroup.save()
        self.stdout.write(self.style.SUCCESS('舆论管理猿创建完成'))

        # 管理员组
        # 上面两个权限返回的都是queryset，需要用union进行连接
        admin_permissions = edit_permissions.union(manage_permissions)
        adminGroup = Group.objects.create(name='管理猿')
        adminGroup.permissions.set(admin_permissions)
        adminGroup.save()
        # 下面的命令是一个打印操作,如果成功打印出hello world,那么这个命令就是创建成功了
        self.stdout.write(self.style.SUCCESS('管理员嗒嗒创建完成'))
