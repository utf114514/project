from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from note.models import Note
from user.models import User
# Create your views here.
def check_log(fu):
    def wrap(request, *args, **kwargs):
        if 'username' not in request.session or 'uid' not in request.session:
            c_username = request.COOKIES.get('username')
            c_uid=request.COOKIES.get('uid')
            if not c_username or not c_uid:
                return HttpResponseRedirect('/user/login')
            else:
                try:
                    User.objects.get(username=c_username)
                except Exception as c:
                    print('有用户尝试写入非法session')
                    return HttpResponse('你的COOKIES不合法,请尝试重新登陆')
                request.session['username'] = c_username
                request.session['uid'] = c_uid
                return fu(request, *args, **kwargs)
        return fu(request, *args, **kwargs)
    return wrap
@check_log
def add_note(request):
    if request.method=='GET':
        return render(request,'note/add_note.html')
    elif request.method=='POST':
        uid=request.session['uid']
        title = request.POST['title']
        content = request.POST['content']
        Note.objects.create(title=title, content=content, user_id=uid)
        return HttpResponse('笔记添加成功')