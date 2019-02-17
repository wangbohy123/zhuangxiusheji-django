from django.shortcuts import render, redirect
from django.template import loader, RequestContext
from django.db.models import Max
from django.http import *
from .models import *

def index(request):
    # 主页的请求
    user_kind = request.session.get('user_kind')
    if user_kind == 'ordinary_user':
        return redirect('/user/index_for_user/')
    elif user_kind == 'company_user':
        return redirect('/user/index_for_company/')
    return render(request, 'index.html')

def index_for_user(request):
    # 用户主页的请求
    uid = request.session.get('uid', default=None)
    user = Ordinary_User.users.get(id=uid)
    context = {
        'uname': user.account_number,
    }
    return render(request, 'index_for_user.html', context)

def index_for_comapny(request):
    # 公司主页的请求
    uid = request.session.get('uid', default=None)
    user = Company_User.comanyUsers.get(id=uid)
    context = {
        'uname': user.account_number,
    }
    return render(request, 'index_for_company.html', context)

def gallery(request):
    # 样例演示
    return render(request, 'gallery.html')

def select_kind(request):
    # 注册前选择用户种类
    return render(request, 'select_kind.html')

def kind_handel(request):
    # 根据用户种类返回相应注册页面
    post = request.POST
    user_kind = post.get('user_kind')
    if user_kind == 'ordinary_user':
        return render(request, 'register_for_ordinary.html')
    elif user_kind == 'company_user':
        return render(request, 'register_for_company.html')

def register(request):
    # 普通用户的注册
    buf = verifycode(request)
    image = buf.getvalue()
    context = {
        'image':image,
    }
    return render(request, 'register_for_ordinary.html')

def login(request):
    # 登陆页面的请求
    buf = verifycode(request)
    image = buf.getvalue()
    context = {
        'image':image,
    }
    return render(request, 'login.html', context)

def login_handel(request):
    # 登录会话
    from hashlib import sha1
    post = request.POST
    uname = post.get('uname')
    upwd = post.get('upwd')
    user_kind= post.get('user_kind')
    code = post.get('verifycode')
    verifycode = request.session['verifycode']
    s1 = sha1()
    s1.update(upwd.encode('utf-8'))
    pwd = s1.hexdigest()
    # if code != verifycode:
    #     return HttpResponse('验证码错误')
    if user_kind == 'ordinary_user':
        user = Ordinary_User.users.filter(account_number=uname)
        if len(user) == 1:
            try:
                temp = Ordinary_User.users.get(account_number=uname, account_passWord=pwd)
                print(temp.account_number)
                id = temp.id
            except:
                return HttpResponse('密码错误')
            request.session['uid'] = id
            request.session['user_kind'] = user_kind
            return redirect('/user/index_for_user/')
        else:
            return redirect('/user/login/')

    elif user_kind == 'company_user':
        user = Company_User.comanyUsers.filter(account_number=uname)
        if len(user) == 1:
            try:
                temp = Company_User.comanyUsers.get(account_number=uname, account_passWord=pwd)
                print(temp.account_number)
                id = temp.id
            except:
                return HttpResponse('密码错误')
            request.session['uid'] = id
            request.session['user_kind'] = user_kind
            return redirect('/user/index_for_company/')
        else:
            return redirect('/user/login/')

    else:
        return HttpResponse('请输入用户种类')

def register_handel_forOrd(request):
    # 用户注册
    from hashlib import sha1
    post = request.POST
    uname = post.get('uname')
    upwd = post.get('upwd')
    cpwd = post.get('cpwd')
    mail = post.get('mail', default='123@qq.com')
    user_kind = post.get('user_kind')
    if upwd != cpwd:
        return redirect('/user/register/')
    # 加密
    s1 = sha1()
    s1.update(upwd.encode('utf-8'))
    pwd = s1.hexdigest()
    if user_kind == 'ordinary_user':
        if Ordinary_User.users.if_has(uname):
            return HttpResponse('repeated')
        o_user = Ordinary_User.users.create(uname, pwd, mail)
        return redirect('/user/login/')

def register_handel_forCom(request):
    # 公司注册
    from hashlib import sha1
    post = request.POST
    uname = post.get('uname')
    upwd = post.get('upwd')
    cpwd = post.get('cpwd')
    name = post.get('company_name')
    mail = post.get('mail', default='123@qq.com')
    user_kind = post.get('user_kind')
    company_text = post.get('company_text')
    company_num = post.get('company_num')
    price = post.get('price')
    style = post.get('style')
    images = []
    image01 = request.FILES.get('image01')
    images.append(image01)
    image02 = request.FILES.get('image02')
    images.append(image02)
    image03 = request.FILES.get('image03')
    images.append(image03)
    image04 = request.FILES.get('image04')
    images.append(image04)
    if upwd != cpwd:
        return redirect('/user/register/')
    # 加密
    s1 = sha1()
    s1.update(upwd.encode('utf-8'))
    pwd = s1.hexdigest()
    if user_kind == 'company_user':
        if Company_User.comanyUsers.if_has(uname):
            return HttpResponse('repeated')

        new_user = Company_User.comanyUsers.create(uname, pwd, name, mail, company_num, company_text, style, price)
        for image in images:
            newImage = CompanyImage(image=image, company=new_user)
            newImage.save()
        return redirect('/user/login/')
    else:
        return HttpResponse('error')


def del_session(request):
    # 清除会话的功能 登出函数
    # request.session.flush()
    del request.session['uid']
    del request.session['user_kind']
    return redirect('/user/index/')

def verifycode(request):
    # 产生验证码的函数
    from PIL import Image, ImageDraw, ImageFont
    import random
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 255)
    width = 100
    height = 25
    im = Image.new('RGB', (width, height), bgcolor)
    draw = ImageDraw.Draw(im)
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    font = ImageFont.truetype("Dengb.ttf", 16)
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    del draw
    request.session['verifycode'] = rand_str
    from io import StringIO,BytesIO
    buf = BytesIO()
    im.save(buf, 'png')
    return HttpResponse(buf.getvalue(), 'image/png')

def aboutUs(request):

    return render(request, 'about.html')

