# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from public.auth.base import AbstractUser
from public.base import BaseModel


class User(BaseModel, AbstractUser):

    username = models.CharField(verbose_name=_(u'User Name'), max_length=30, unique=True)
    email = models.EmailField(_(u'email address'), blank=True)
    is_active = models.BooleanField(_(u'active'), default=True)
    date_joined = models.DateTimeField(_(u'date joined'), default=timezone.now, editable=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def check_password(self, raw_password):
        return super(User, self).check_password(raw_password)
        # return True

    class Admin(BaseModel.Admin):
        list_display = ('username', 'last_login')
        actions = []
        creation_form = 'system.forms.UserCreationForm'
        change_form = 'system.forms.UserChangeForm'

    class Meta:
        app_label = "system"
        verbose_name = _(u'User')
        verbose_name_plural = verbose_name