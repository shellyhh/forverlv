# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from system.models import User


def create_superuser(signal, sender, **kwargs):

    if User in (v for k, v in sender.models.iteritems()):
        admin = User.objects.filter(username='admin')
        if not admin:
            User.objects.create_superuser('admin', 'admin@qq.com', 'admin')