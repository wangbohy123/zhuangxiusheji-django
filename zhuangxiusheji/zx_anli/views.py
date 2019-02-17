from django.shortcuts import render, redirect
from zx_user.models import Company_User, Ordinary_User, CompanyImage
from .models import Anli, CaseImage, Suggestions, Comments

def show_company(request):
    companies = Company_User.comanyUsers.get_queryset()
    uid = request.session.get('uid', default=None)
    user_kind = request.session.get('user_kind', default=0)
    uname = ''
    if user_kind == 'ordinary_user':
        uname = Ordinary_User.users.get(id=uid)
    print(companies)

    if request.method == 'POST':
        post = request.POST
        price = post.get('price')
        style = post.get('style')
        companies = Company_User.comanyUsers.filter(paice_range=price, style=style)
        pass
    comtext = {
        'companies':companies,
        'uname':uname,
    }
    return render(request, 'showCompanies.html', comtext)

def show_detail(request):
    uid = request.GET['id']
    company = Company_User.comanyUsers.get(id=uid)
    companyImages = company.companyimage_set.all()
    context = {
        'company':uid,
        'name':company.company_name,
        'companyNum':company.company_num,
        'mail':company.account_mail,
        'examine':company.examine,
        'index':company.account_describe,
    }
    i = 1
    for image in companyImages:
        context['image' + str(i)] = image.image.url
        i += 1
    return render(request, 'show_detail.html', context)

def give_case(request):
    # 基本用户给公司提交案例
    uid = request.POST['companyid']
    context = {
        'company':uid
    }
    return render(request, 'writeCase.html', context)

def case_handel(request):

    uid = request.session.get('uid', default=None)
    post = request.POST
    case_name = post.get('case_name')
    companyid = post.get('companyid')
    case_text = post.get('case_text')
    area = post.get('area')
    case_style = post.get('case_style')
    huxing = post.get('huxing')
    user = Ordinary_User.users.get(id=uid)
    index = {
        'name': case_name,
        'companyid': companyid,
        'text': case_text,
        'user': user,
        'area':area,
        'case_style':case_style,
        'huxing':huxing,
    }
    newCase = Anli.cases.create(index)

    # 存储图片
    file01 = request.FILES.get('case_image01', default='')
    file02 = request.FILES.get('case_image02', default='')
    file03 = request.FILES.get('case_image03', default='')
    images = [file01, file02, file03]
    for image in images:
        if image != '':
            caseImage = CaseImage(image=image, case=newCase)
            caseImage.save()

    return redirect('/anli/showCompanies')

def check_case(request):
    # 查看用户案例  通过get方法得到id
    cid = request.GET['cid']
    case = Anli.cases.get(id=cid)
    caseName = case.anli_name
    caseImages = case.caseimage_set.all()
    caseText = case.anli_describe
    suggestion = case.suggestions_set.all()
    suggNum = len(suggestion)
    comments = case.comments_set.all()
    commNum = len(comments)
    # image = getImage(caseImage)
    context = {
        'caseName':caseName,
        'caseImage':caseImages,
        'caseText':caseText,
        'suggestion':suggestion,
        'suggNum':suggNum,
        'comments':comments,
        'commNum':commNum,
        'cid':cid,
    }
    return render(request, 'showCase.html', context)

def write_comment(request):
    # 写评论的请求
    post = request.POST
    cid = post.get('cid')
    context = {
        'cid':cid
    }
    return render(request, 'writeComment.html', context)

def comment_handel(request):
    # 产生新评论
    post = request.POST
    text = post.get('comment_text')
    cid = post.get('cid')
    case = Anli.cases.get(id=cid)
    comment = Comments(comment=text, anli=case)
    comment.save()
    return redirect('/anli/user_case/')

def getImage(image):
    from PIL import Image
    from io import BytesIO
    buf = BytesIO()
    # buf = image
    im = Image.fromstring(image)
    im.save(buf, 'png')

def user_case(request):
    # 展示案例
    cases = Anli.cases.all()
    if request.method == 'POST':
        post = request.POST
        area = post.get('area')
        case_style = post.get('case_style')
        huxing = post.get('huxing')
        cases = Anli.cases.filter(area=area, case_style=case_style, huxing=huxing)
    context = {
        'cases':cases,
    }
    return render(request, 'userCase.html', context)

def company_case(request):
    # 公司查看案例
    uid = request.session.get('uid', default=None)
    user_kind = request.session.get('user_kind', default=None)

    if user_kind == 'company_user':
        cases = Anli.cases.filter(company=uid)
        print(cases, type(cases))
        context = {
            'cases':cases,
        }
        return render(request, 'companyCase.html', context)

def company_suggestion(request):
    # 公司用户对案例提交反馈意见
    cid = request.GET['cid']
    case = Anli.cases.get(id=cid)
    caseName = case.anli_name
    caseImages = case.caseimage_set.all()
    caseText = case.anli_describe
    answer = case.answer
    sugg = ''
    if answer == False:
        sugg = ''
    elif answer == True:
        suggestion = Suggestions.objects.get(anli_id=case)
        sugg = suggestion.suggestion
        print(sugg)
    context = {
        'caseName': caseName,
        'caseImage': caseImages,
        'caseText': caseText,
        'sugg': sugg,
        'answer':answer,
        'cid':cid,
    }

    return render(request, 'submitSuggestion.html', context)

def suggestion_handel(request):
    # 创建新意见
    post = request.POST
    text = post.get('suggestion')
    cid = post.get('cid')
    uid = request.session.get('uid', default=None)
    com = Company_User.comanyUsers.get(id=uid)
    case = Anli.cases.get(id=cid)
    sugg = Suggestions(suggestion=text, anli=case, company=com)
    sugg.save()
    case.answer = True
    case.save()
    # /user_center/corporate/
    return redirect('/anli/company_case/')
