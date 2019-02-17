from django.db import models

class Ordinary_UserManager(models.Manager):

    def create(self, accountnum, password, mail):
        # 写创建对象的方法 创建对象时可以调用该类方法
        ord = Ordinary_User()
        ord.account_number = accountnum
        ord.account_passWord = password
        ord.account_mail = mail
        ord.save()
        return ord

    def if_has(self, uname):
        try:
            self.get(account_number=uname)
        except:
            return False
        return True

    def modify_password(self, uid, newpass, newmail):
        # 修改信息的时候调用该函数
        user = self.filter(id=uid)

        if newmail != '':
            user.update(account_mail = newmail)

        user.update(account_passWord=newpass)
        return True

class Company_UserManager(models.Manager):

    def create(self, accountnum, password, company_name ,mail, company_num, account_describe, style, paice):
        ord = Company_User()
        ord.account_number = accountnum
        ord.company_name = company_name
        ord.account_passWord = password
        ord.account_mail = mail
        ord.account_describe = account_describe
        ord.company_num = company_num
        ord.style = style
        ord.paice_range = paice
        ord.save()
        return ord

    def if_has(self, uname):
        try:
            self.get(account_number=uname)
        except:
            return False
        return True

    def modify_password(self, uid, canshu):
        # 修改信息的时候调用该函数
        user = self.filter(id=uid)
        for key in canshu:
            if canshu[key] != '':
                if key == 'account_passWord':
                    user.update(account_passWord=canshu[key])
                elif key == 'account_mail':
                    user.update(account_mail=canshu[key])
                elif key == 'company_name':
                    user.update(company_name=canshu[key])
                elif key == 'company_num':
                    user.update(company_num=canshu[key])
                elif key == 'account_describe':
                    user.update(account_describe=canshu[key])

        user.update(examine='W')
        user.update(if_passed=False)
        return True


class Ordinary_User(models.Model):
    # 基本用户
    account_number = models.CharField(max_length=20) # 账号
    account_passWord = models.CharField(max_length=40)# 密码
    account_mail = models.CharField(max_length=30)#邮箱
    users = Ordinary_UserManager()

    def __str__(self):
        return self.account_number

    class Meta:
        # 元选项 修改表的名称
        db_table = 'ordinary_user' # 表名
        ordering = ['id'] # 指定查询的排序规则

class Company_User(models.Model):
    # 公司用户
    account_number = models.CharField(max_length=20)  # 账号
    account_passWord = models.CharField(max_length=40)  # 密码
    account_mail = models.CharField(max_length=30)  # 邮箱
    company_name = models.CharField(max_length=20) # 公司名
    company_num = models.CharField(max_length=30) # 营业执照号码
    account_describe = models.TextField(max_length=2000) # 公司描述  审核的依据
    examine = models.CharField(max_length=20, default='W', choices=(('W','审核中'),('Y','审核通过'),('N','未通过'))) # 审核状态
    casefor = models.TextField(max_length=200, default='') # 对该公司的备注
    if_passed = models.BooleanField(default=False) # 审核是否通过
    style = models.CharField(max_length=30, choices=(('O','欧美风格'),('D','东方风格')) )
    paice_range = models.CharField(max_length=30, choices=(('0-5000','5000元以下'), ('5000-10000', '5000到10000元'),('10000-','10000元以上')) )
    comanyUsers = Company_UserManager()

    def __str__(self):
        return self.account_number

    class Meta:
        # 元选项 修改表的名称
        db_table = 'company_user'
        ordering = ['id'] # 指定查询的排序规则

class CompanyImage(models.Model):
    company = models.ForeignKey(Company_User)
    image = models.ImageField(upload_to='company_images/', null=False, blank=True)

    class Meta:
        db_table = 'company_images'
