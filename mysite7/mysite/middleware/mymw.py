from django.core import mail
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
import re
import traceback
from django.conf import settings


class Mymw(MiddlewareMixin):
    def process_request(self, request):
        print('process_request is ok')
        return None

    def process_view(self, request, callback, callback_args, callback_kwargs):
        print('process_view is ok')
        return None

    def process_response(self, request, response):
        # print('process_response is ok')
        return response


class Mymw2(MiddlewareMixin):
    def process_request(self, request):
        # print('process_request2 is ok')
        return None

    def process_view(self, request, callback, callback_args, callback_kwargs):
        # print('process_view2 is ok')
        return None

    def process_response(self, request, response):
        # print('process_response2 is ok')
        return response


class VisitLimit(MiddlewareMixin):
    visit_t = {}

    def process_request(self, request):
        ip = request.META['REMOTE_ADDR']
        path_url = request.path_info
        if not re.match('^/test_cache', path_url):
            return None
        else:
            times = self.visit_t.get(ip, 0)
            print('ip', ip, times)
            self.visit_t[ip] = times + 1
            if times < 5:
                return None
            return HttpResponse('您已经访问了' + str(self.visit_t.get(ip)) + '次访问禁止')


class EXMW(MiddlewareMixin):
    def process_exception(self, request, exception):
        print(exception)
        print(traceback.format_exc())
        mail.send_mail(subject='mysite 错误', message=traceback.format_exc(), from_email='2102014866@qq.com',
                       recipient_list=settings.EX_EMAIL)
        return HttpResponse('-----对不起当前网页错误:(')
