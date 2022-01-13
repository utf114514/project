import hashlib

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .models import User


# Create your views here.
def reg_view(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password_1 = request.POST['password_1']
        password_2 = request.POST['password_2']
        if password_1 != password_2:
            return HttpResponse('两次密码输入不一致')
        old_users = User.objects.filter(username=username)
        if old_users:
            return HttpResponse('用户名已注册')
        m = hashlib.md5()
        m.update(password_1.encode())
        password = m.hexdigest()
        try:
            olo = User.objects.create(username=username, password=password)
        except Exception as e:
            print(e + 'error')
            return HttpResponse('用户名已注册')
        request.session['username'] = username
        request.session['id'] = olo.id

        return HttpResponseRedirect('/index')


def login_view(request):
    if request.method == 'GET':
        if request.session.get('username') and request.session.get('uid'):
            return HttpResponseRedirect('/index')
        c_username = request.COOKIES.get('username')
        c_uid = request.COOKIES.get('uid')
        try:
            User.objects.get(username=c_username)
        except Exception as c:
            if c_username or c_uid:
                print('有用户尝试写入非法session')
                return HttpResponse('你的COOKIES不合法,请尝试重新登陆')
            elif not c_username and not c_uid:
                return HttpResponseRedirect('/user/login')
        if c_username and c_uid:
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            return HttpResponseRedirect('/index')
        return render(request, 'login.html')

    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except Exception as a:
            print(a + 'error')
            return HttpResponse('用户名或密码错误')
        m = hashlib.md5()
        m.update(password.encode())
        if m.hexdigest() != user.password:
            return HttpResponse('用户名或密码错误')
        request.session['username'] = username
        request.session['uid'] = user.id
        rest = HttpResponseRedirect('/index')
        if 'remember' in request.POST:
            rest.set_cookie('username', username, 3600 * 24 * 3)
            rest.set_cookie('uid', user.id, 3600 * 24 * 3)
        return rest


def logout_view(request):
    resp = None
    if 'username' in request.session:
        del request.session['username']
    if 'uid' in request.session:
        del request.session['uid']
        resp = HttpResponseRedirect('/index')
    if 'username' in request.COOKIES:
        resp.delete_cookie('username')
    if 'uid' in request.COOKIES:
        resp.delete_cookie('uid')
    return resp
