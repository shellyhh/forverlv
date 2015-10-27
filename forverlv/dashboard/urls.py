# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from django.conf.urls import url
from django.template.response import TemplateResponse


def index(request, app_label):
    from public.functions import get_app_list
    apps = get_app_list()
    context = {
        'apps': apps,
        'app_label': app_label
    }
    return TemplateResponse(request, 'dashboard.html', context)

urlpatterns = [
    url(r'^$', view=index, kwargs={'app_label': 'dashboard'})
]