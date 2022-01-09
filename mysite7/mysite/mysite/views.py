from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
import time
import csv
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from upload_app .models import Content

@cache_page(15)
def test_cache(request):
    t = time.time()
    print('view in')
    return HttpResponse('time is %s' % t)


def test_csrf(request):
    if request.method == 'GET':
        return render(request, 'test_csrf.html')
    elif request.method == 'POST':
        return HttpResponse('post is ok :)')


def test_page(request):
    page_num = int(request.GET.get('page', 1))
    if page_num <= 0:
        return HttpResponseRedirect('/test_page')
    all_data = ['a', 'b', 'c', 'd', 'e']
    paginator = Paginator(all_data, 2)
    page = paginator.page(page_num)
    return render(request, 'test_page.html', locals())


def test_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="tset.csv"'
    all_data = ['a', 'b', 'c', 'd']
    writer = csv.writer(response)
    writer.writerow(all_data)
    return response


def make_page_csv(request):
    page_num = int(request.GET.get('page', 1))
    if page_num <= 0:
        return HttpResponseRedirect('/test_page')
    all_data = ['a', 'b', 'c', 'd', 'e']
    paginator = Paginator(all_data, 2)
    page = paginator.page(page_num)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="page-%s.csv"' % page_num
    writer = csv.writer(response)
    for b in page:
        writer.writerow([b])
    return response


@csrf_exempt
def test_upload(request):
    if request.method == 'GET':

        return render(request, 'test_upload.html')
    elif request.method == 'POST':
        title = request.POST.get('title')
        myfile = request.FILES['xiaohuangyo']
        Content.objects.create(title=title, picture=myfile)
        return HttpResponse('ok')
def test_(request):
    li=[1,2,2,3,4,5,6,7,8]
    return render(request, 'test.html', locals())