from django.shortcuts import render,HttpResponse
from app01 import models

# Create your views here.


def user_info(request, pk):
    obj = models.UserInfo.objects.filter(pk=pk)[0]
    return render(request, 'user_info.html', {'obj': obj})
