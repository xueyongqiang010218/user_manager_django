from django.shortcuts import render,redirect,HttpResponse
from app01 import models
# def login(request):
#     message = ''
#     if request.method == "POST":
#         user = request.POST.get('user')
#         pwd = request.POST.get('pwd')
#         c = models.Administratror.objects.filter(username=user,password=pwd).count()
#         if c:
#             #认证成功，设置cookies
#             rep = redirect('/index.html/')
#             rep.set_cookie('username',user,max_age=10)
#             return rep
#         else:
#             message = '用户名或密码错误'
#     return render(request,'login.html',{'msg':message})
#
# def index(request):
#     #如果用户已经登入，获取当前登入的用户名
#     #否则，返回登录页面
#     username = request.COOKIES.get('username')
#     print(username)
#     if username :
#         return  render(request,'index.html',{'username':username})
#     else:
#         return redirect('/login.html/')

#FBV
def login(request):
    message = ""
    v = request.session
    print(type(v))
    if request.method == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        c = models.Administrator.objects.filter(username=user,password=pwd).count()
        if c:
            request.session['is_login'] = True
            request.session['username'] = user
            rep = redirect('/index.html')
            return rep
        else:
            message = '用户名或者密码错误'
    obj = render(request,'login.html',{'msg':message})
    return obj

def  logout(request):
    request.session.clear()
    return redirect('/login.html')

def auth(func):
    def inner(request,*args,**kwargs):
        is_login = request.session.get('is_login')
        if is_login:
            return func(request,*args,**kwargs)
        else:
            return redirect('/login.html')
    return inner

@auth
def index(request):
    current_user = request.session.get('username')
    return render(request,'index.html',{'username':current_user})

def handle_classes(request):
    # for i in range(1000):
    #     models.Classes.objects.create(caption='caption%s'%i)
    from utils.page import page_paginator
    if request.method == 'GET':
        blogs_all_list = models.Classes.objects.all()
        page_of_blogs,page_range = page_paginator(request,blogs_all_list)
        current_user = request.session.get('username')
        return render(request,'classes.html',
                      {'username':current_user,'blogs':page_of_blogs.object_list,'page_of_blogs':page_of_blogs,'page_range': page_range})

    elif request.method =="POST":
        import json
        response_dict = {'status':True,'error':None,'data':None}
        caption = request.POST.get('caption',None)
        print(caption)
        if caption:
            obj = models.Classes.objects.create(caption=caption)
            response_dict['data'] = {'id':obj.id,'caption':obj.caption}
        else:
            response_dict['status'] = False
            response_dict['error'] = '标题不能为空'
        return HttpResponse(json.dumps(response_dict))


def handle_student(request):
    is_login = request.session.get('is_login')
    if is_login:
        current_user = request.session.get('username')
        return render(request, 'student.html', {'username': current_user})
    else:
        return redirect('/login.html')


def handle_teacher(request):
    is_login = request.session.get('is_login')
    if is_login:
        current_user = request.session.get('username')
        return render(request, 'teacher.html', {'username': current_user})
    else:
        return redirect('/login.html')