from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
# Create your views here.


def login(request):

    return HttpResponse('login page')



class UrlParamsToView(View):
    def get(self, request, id):
        pass





