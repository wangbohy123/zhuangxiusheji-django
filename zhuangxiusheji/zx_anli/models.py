from django.db import models
from zx_user.models import Ordinary_User, Company_User

class AnliManager(models.Manager):

    def create(self, index):
        new = Anli()
        new.company = index['companyid']
        new.anli_name = index['name']
        new.anli_describe = index['text']
        new.ordinary_user = index['user']
        new.area = index['area']
        new.case_style = index['case_style']
        new.huxing = index['huxing']
        new.save()
        return new

# 用户提交的案例类
class Anli(models.Model):

    anli_name = models.CharField(max_length=30)
    ordinary_user = models.ForeignKey(Ordinary_User) # 外键是普通用户
    anli_describe = models.TextField(max_length=2000)
    company = models.IntegerField(default=0)
    answer = models.BooleanField(default=False)
    score = models.IntegerField(default=0)

    area = models.CharField(max_length=30, choices=(('0-100','100平米以下'), ('100+', '100平米以上') ))
    case_style = models.CharField(max_length=30, choices=(('O','欧美风格'),('D','东方风格')) )
    huxing = models.CharField(max_length=30, choices=(('1','一室一厅'), ('2','两室两厅'),('3', '三室两厅'),('4','其他')) )
    cases = AnliManager()

    def __str__(self):
        return self.anli_name

    class Meta:
        db_table = 'anli'

# 评论类
class Comments(models.Model):
    # 用户发表的评论
    comment = models.TextField(max_length=2000)
    # 外键是评论的案例
    anli = models.ForeignKey(Anli)

    class Meta:
        db_table = 'commments'

# 公司对案例的意见类
class Suggestions(models.Model):

    suggestion = models.TextField(max_length=2000)
    anli = models.ForeignKey(Anli)
    company = models.ForeignKey(Company_User)

    class Meta:
        db_table = 'suggestions'

class CaseImage(models.Model):
    case = models.ForeignKey(Anli)
    image = models.ImageField(upload_to='anli_images/', null=False, blank=True)
    imageName = models.CharField(max_length=20, default='')
    class Meta:
        db_table = 'images'
