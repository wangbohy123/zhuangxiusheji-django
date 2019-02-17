from django.shortcuts import render,redirect
from zx_user.models import Ordinary_User, Company_User
from zx_anli.models import Anli, Comments, Suggestions
from django.http import HttpResponse
def user_center(request):
    # 用户中心的处理
    return render(request, '01.html')

def user_center_company(request):
    uid = request.session.get('uid', default=None)
    user_kind = request.session.get('user_kind', default=0)
    if user_kind == 'company_user':
        user = Company_User.comanyUsers.get(id=uid)
        context = {
            'user':user
        }
        return render(request, '02.html', context)

def personal(request):
    uid = request.session.get('uid', default=None)
    user_kind = request.session.get('user_kind', default=0)

    if user_kind == 'ordinary_user':
        # result表示查找出来的普通用户
        user = Ordinary_User.users.get(id=uid)
        cases = user.anli_set.all()
        # if len(cases) == 0:
        #     cases = '还没有提交案例'
        context = {
            'uname': user.account_number,
            'user_kind': user_kind,
            'mail':user.account_mail,
            'cases':cases,
        }
        return render(request, 'personal.html', context)

def modify_personal(request):
    uid = request.session.get('uid', default=None)
    user_kind = request.session.get('user_kind', default=0)

    if user_kind == 'ordinary_user':
        # result表示查找出来的普通用户
        user = Ordinary_User.users.get(id=uid)
        context = {
            'uname': user.account_number,
            'user_kind': user_kind,
            'mail':user.account_mail,
        }
        return render(request, 'modify_personal.html', context)

def modify_personal_handel(request):
    from hashlib import sha1
    post = request.POST
    user_kind = post.get('user_kind')
    uid = request.session.get('uid', default=None)
    if user_kind == 'ordinary_user':

        upwd = post.get('upwd')
        cpwd = post.get('cpwd')
        mail = post.get('email')
        if upwd != cpwd:
            return redirect('/user_center/modify_personal/')
        s1 = sha1()
        s1.update(upwd.encode('utf-8'))
        pwd = s1.hexdigest()
        if Ordinary_User.users.modify_password(uid, pwd, mail):
            return redirect('/user_center/personal/')

def corporate(request):
    uid = request.session.get('uid', default=None)
    user_kind = request.session.get('user_kind', default=0)

    if user_kind == 'company_user':
        user = Company_User.comanyUsers.get(id=uid)
        examime = ''.join(user.examine.split())
        if examime == 'Y':
            examime = '审核通过'
        elif examime == 'W':
            examime = '审核中'
        elif examime == 'N':
            examime = '审核不通过'
        companyImages = user.companyimage_set.all()
        context = {
            'uname': user.account_number,
            'name': user.company_name,
            'user_kind': '公司用户',
            'companyNum': user.company_num,
            'mail': user.account_mail,
            'if_passed': user.if_passed,
            'examine': examime,
            'index': user.account_describe,
            'remarks': user.casefor,
            'companyImages': user.companyimage_set.all(),
        }
        i = 1
        for image in companyImages:
            context['image'+str(i)] = image.image.url
            i += 1

        return render(request, 'corporate.html', context)

def modify_company(request):
    uid = request.session.get('uid', default=None)
    user_kind = request.session.get('user_kind', default=0)
    if user_kind == 'company_user':
        user = Company_User.comanyUsers.get(id=uid)
        examime = ''.join(user.examine.split())
        if examime == 'Y':
            examime = '审核通过'
        elif examime == 'W':
            examime = '审核中'
        elif examime == 'N':
            examime = '审核不通过'
        context = {
            'uname':user.account_number,
            'name':user.company_name, # 公司名
            'user_kind':'公司用户',
            'companyNum':user.company_num,
            'mail':user.account_mail,
            'if_passed':user.if_passed, # 是否通过
            'examine':examime, # 审核状态
            'index':user.account_describe, # 公司描述
            'remarks':user.casefor, # 备注  （不通过原因）
        }
        return render(request, 'modify_corporate.html', context)

def modify_company_handel(request):
    from hashlib import sha1
    post = request.POST
    user_kind = post.get('user_kind')
    uid = request.session.get('uid', default=None)

    if user_kind == 'company_user':
        upwd = post.get('upwd')
        cpwd = post.get('cpwd')
        mail = post.get('mail')
        name = post.get('name')
        companyNum = post.get('companyNum')
        company_text = post.get('company_text')

        if upwd != cpwd:
            return redirect('/user_center/modify_personal/')
        s1 = sha1()
        s1.update(upwd.encode('utf-8'))
        pwd = s1.hexdigest()
        canshu = {
            'account_passWord':pwd,
            'account_mail':mail,
            'company_name':name,
            'company_num':companyNum,
            'account_describe':company_text,
        }
        if Company_User.comanyUsers.modify_password(uid, canshu):
            return redirect('/user_center/corporate/')
        else:
            return HttpResponse('修改失败')

