# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_migrate
from .management import create_superuser


class SystemConfig(AppConfig):
    name = 'system'
    verbose_name = _(u"System")

    def ready(self):
        post_migrate.connect(create_superuser)