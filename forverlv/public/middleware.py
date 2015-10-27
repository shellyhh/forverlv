# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect, HttpResponse
import json


class BaseMiddleware(object):
    def __init__(self):
        self.login_url = settings.LOGIN_URL
        self.logout_url = settings.LOGOUT_URL

    def redirect_to_login(self, request):
        if request.is_ajax():
            return HttpResponse(json.dumps({'ret': 'timeout', 'url': self.login_url}))
        else:
            path = "{0}?{1}={2}".format(self.login_url, REDIRECT_FIELD_NAME, request.path)
            return HttpResponseRedirect(path)


class SessionExpiryMiddleware(BaseMiddleware):

    def process_request(self, request):

        if request.path not in (self.login_url, self.logout_url):
            session = request.session
            empty = session.is_empty()
            expiry_date = session.get_expiry_date()
            if empty or expiry_date < timezone.now():
                return self.redirect_to_login(request)


class LoginRequiredMiddleware(BaseMiddleware):

    def process_request(self, request):
        if request.path not in (self.login_url, self.logout_url):
            user = request.user
            if not user.is_authenticated():
                return self.redirect_to_login(request)