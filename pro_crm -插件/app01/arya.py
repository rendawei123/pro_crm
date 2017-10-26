#!/usr/bin/env python
# -*- coding:utf-8 -*-

from arya.service import sites
from . import models
from django.shortcuts import render, HttpResponse


class UserInfoConfig(sites.AryaConfig):

    def detail_view(self, request, pk):
        obj = self.model_class.objects.filter(pk=pk)[0]
        return render(request, 'user_info.html', {'obj': obj})

    def extra_urls(self):
        from django.conf.urls import url
        app_model_name = self.model_class._meta.app_label, self.model_class._meta.model_name
        urlpatterns = [
            url(r'^(.+)/detail/$', self.wrapper(self.detail_view), name="%s_%s_delete" % app_model_name),
        ]
        return urlpatterns

sites.site.register(models.UserInfo, UserInfoConfig)


class Department(sites.AryaConfig):
    list_display = ['title', ]

sites.site.register(models.Department, Department)
