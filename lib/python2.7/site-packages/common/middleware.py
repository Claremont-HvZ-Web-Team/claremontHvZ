# coding: utf-8
from django.shortcuts import redirect
from django.contrib import messages

class UnderConstructionMiddleware(object):
    def process_request(self, request):
        if request.method == 'POST':
            messages.error(request, u'Извините. Сайт переезжает на другой сервер. Все изменения данных временно запрещены')
            return redirect(request.get_full_path())
        else:
            return None
