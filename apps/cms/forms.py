from django import forms
from apps.cms.models import News
from apps.forms import FormMixin


# 编辑新闻分类表单
class EditCategoryForm(forms.Form):
    pk = forms.IntegerField()
    name = forms.CharField(max_length=100)


#  创建一个表单类，来对新闻发布页面的数据进行提取，发布时间不需要，作者也不需要，分类也不需要(为了实验一下，暂时需要)
#  分类不需要是因为需要重新定义，要提取一个整型的数据
#  在此实验了分类这个字段要不要重新定义，结果是可以不需要重新定义
class WriteNewsForm(forms.ModelForm, FormMixin):
    # category = forms.IntegerField()

    class Meta:
        model = News
        # exclude = ['author', 'pub_time', 'category']
        exclude = ['author', 'pub_time']


# 编辑新闻表单
class EditNewsForm(forms.ModelForm, FormMixin):
    id = forms.IntegerField()

    class Meta:
        model = News
        exclude = ['author', 'pub_time']
