# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from django.shortcuts import render
from public.page.base import page_generator
from django.apps import apps
from public.functions import get_app_list


def page_view(request, app_label, model_name):
    heads, actions = page_generator(request, app_label, model_name)
    app_list = get_app_list()
    context = dict(
        app_label=app_label,
        model_name=model_name,
        heads=heads,
        actions=actions,
        apps=app_list
    )
    templates = [
        '{0}_{1}.html'.format(app_label.lower(), model_name.lower()),
        'model_page.html',
        'public/web_base.html'
    ]
    return render(request, templates, context)


def grid_view(request, app_label, model_name):
    from public.views.changelist_view import ChangelistView
    model = apps.get_model(app_label, model_name)
    cl_view = ChangelistView(request, model)
    return cl_view.changelist_view()


def model_view(request, app_label, model_name, object_id):
    from public.views.model_view import ModelView
    model = apps.get_model(app_label, model_name)
    m_view = ModelView(request, model, object_id)
    return m_view.model_view()


def model_action(request, app_label, model_name, action_name):
    if action_name in ('ModelAdd', ):
        return model_view(request, app_label, model_name, None)
    model = apps.get_model(app_label, model_name)
    action = model.get_action(action_name)
    if action is None:
        return
    action = action(request, model)
    return action.action_view()
