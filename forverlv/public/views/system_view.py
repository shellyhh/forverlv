# -*- coding: utf-8 -*-
__author__ = 'Arvin'


class SystemView(object):

    def index(self, request):
        from django.template.response import TemplateResponse
        from public.functions import get_app_list
        context = {
            'apps': get_app_list(),
            'app_label': 'dashboard'
        }
        template = "dashboard.html"
        return TemplateResponse(request, template, context)

    def login(self, request):
        from public.auth.views import login
        from public.auth.forms import UserAuthenticationForm
        defaults = {
            'authentication_form': UserAuthenticationForm,
            'template_name': 'public/login.html',
        }
        return login(request, **defaults)

    def logout(self, request):
        # from public.auth.views import logout
        from public.auth.views import logout_then_login as logout
        defaults = {}
        return logout(request, defaults)

    def get_urls(self):
        from django.conf.urls import url, include
        urlpatterns = [
            url(r'^$', self.index, name='index'),
            url(r'^accounts/login/$', self.login, name='login'),
            url(r'^accounts/logout/$', self.logout, name='logout'),
        ]
        return urlpatterns

    def urls(self):
        return self.get_urls()


site = SystemView()