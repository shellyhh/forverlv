# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from django.contrib.auth import (REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout)
from public.auth.forms import UserAuthenticationForm
from django.utils.http import is_safe_url
from django.shortcuts import resolve_url
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
import json


def index(request):
    pass


def login(request, template_name='public/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=UserAuthenticationForm,
          current_app=None, extra_context=None):
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())
            return HttpResponse(json.dumps({'ret': 'success', 'redirect_to': redirect_to}))
        else:
            message = {f: e.get_json_data(False) for f, e in form.errors.items()}
            return HttpResponse(json.dumps({'ret': 'failed', 'message': message}))
    else:
        form = authentication_form(request)

    context = {
        'form': form
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context)


def logout(request, next_page=None,
           template_name='public/logged_out.html',
           redirect_field_name=REDIRECT_FIELD_NAME,
           current_app=None, extra_context=None):
    auth_logout(request)
    if next_page is not None:
        next_page = resolve_url(next_page)
    if redirect_field_name in request.POST or redirect_field_name in request.GET:
        next_page = request.POST.get(redirect_field_name,
                                     request.GET.get(redirect_field_name))
        if not is_safe_url(url=next_page, host=request.get_host()):
            next_page = request.path
    if next_page:
        return HttpResponseRedirect(next_page)

    context = {}
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context)


def logout_then_login(request, login_url=None, extra_context=None):
    if not login_url:
        login_url = settings.LOGIN_URL
    login_url = resolve_url(login_url)
    return logout(request, login_url, extra_context=extra_context)