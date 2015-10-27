# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PersonnelConfig(AppConfig):
    name = 'system'
    verbose_name = _(u"Personnel")