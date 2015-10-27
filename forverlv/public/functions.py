# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from django.apps import apps
from django.conf import settings
from django.db import models
# from public.base import BaseModel


def get_app_list():
    app_list = []
    for app_label in (app for app in settings.INSTALLED_APPS if app not in settings.IGNORE_APPS):
        app = apps.get_app_config(app_label)
        app_label = app.name
        app_url = "/{0}/".format(app_label)
        app_dict = dict(app_label=app_label, verbose_name=app.verbose_name,
                        app_url=app_url, models=[])
        ms = app.get_models()
        for m in ms:
            # print app_label, "###############", m
            if issubclass(m, models.Model):
                opts = m._meta
                model_name = m.__name__
                model_dict = dict(
                    model_name=model_name,
                    verbose_name="{0}".format(opts.verbose_name),
                    url="/model/page/{0}/{1}".format(app_label, model_name)
                )
                app_dict['models'].append(model_dict)
        app_list.append(app_dict)
    # print "************", app_list
    return app_list