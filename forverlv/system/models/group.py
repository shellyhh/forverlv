# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from public.base import BaseModel
from public.action.actions import default_actions
from django.contrib.auth.models import Group as AuthGroup


class Group(AuthGroup):

    class Admin(BaseModel.Admin):
        list_display = ('name', )
        actions = default_actions
        creation_form = 'system.forms.GroupCreationFrom'

    class Meta:
        proxy = True
        app_label = 'system'
        verbose_name = "Group"
        verbose_name_plural = verbose_name
        default_permissions = ('browser', 'add', 'change', 'delete')

