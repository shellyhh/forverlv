# -*- coding: utf-8 -*-
__author__ = 'Arvin'


class PageBase(object):
    pass


def get_actions(model):
    actions = []
    for klass in model.__mro__[::-1]:
        admin = getattr(klass, 'Admin', None)
        if admin:
            class_actions = getattr(admin, 'actions', [])
            actions.extend(get_action(action) for action in class_actions)
    actions = filter(None, actions)
    return actions


def bool_format(option):

    return option and 'true' or 'false'


def get_action(action):
    # if issubclass(action, type) and callable(action):
    if type(action) == type and callable(action):
        func = action
        action = dict(
            action_name=func.__name__,
            verbose_name="{0}".format(getattr(func, 'verbose_name') or func.__name__),
            object_unique=bool_format(getattr(func, 'object_unique', False)),
            model_action=bool_format(getattr(func, 'model_action', False)),
            object_action=bool_format(getattr(func, 'object_action', False)),
        )
        return action


def page_generator(request, app_label, model_name):
    from django.apps import apps
    from django.utils.safestring import mark_safe
    import json
    model = apps.get_model(app_label, model_name)
    actions = get_actions(model)
    fields = model._meta.get_fields()
    heads = []
    for field in fields:
        if not getattr(field, 'editable', False):
            continue
        if field.name not in model.Admin.list_display:
            continue
        heads.append({'key': field.name, 'name': "%s" % field.verbose_name})
    heads = mark_safe(json.dumps(heads))
    return heads, actions