# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_migrate
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.management import update_contenttypes
from django.contrib.auth.models import Permission


def create_proxy_permissions(app_config, **kwargs):
    update_contenttypes(app_config, kwargs)
    app_models = app_config.get_models()
    for model in app_models:
        opts = model._meta
        if opts.proxy:
            proxy_model = opts.proxy_for_model
            proxy_opts = proxy_model._meta
            proxy_app_label, proxy_model_name = proxy_opts.app_label, proxy_opts.object_name.lower()
            proxy_ctype = ContentType.objects.get_by_natural_key(proxy_app_label, proxy_model_name)
            app_label, model_name = opts.app_label, opts.object_name.lower()
            ctype = ContentType.objects.get_by_natural_key(app_label, model_name)
            for name, codename in proxy_ctype.permission_set.all().values_list('name', 'codename'):
                if not ctype.permission_set.filter(content_type=ctype, codename=codename):
                    Permission(name=name, content_type=ctype, codename=codename).save()


class PublicConfig(AppConfig):
    name = 'public'
    verbose_name = _(u"Public")

    def ready(self):
        post_migrate.connect(create_proxy_permissions)
        post_migrate.disconnect(update_contenttypes)