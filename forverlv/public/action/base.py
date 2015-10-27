# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from django.forms.models import BaseForm
from collections import OrderedDict
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
import json


class BaseAction(object):
    """
    Action base
    """
    verbose_name = None
    template = None
    position_index = 999
    object_unique = False
    model_action = False
    object_action = False
    help_text = None
    fields = ()

    def __init__(self, request, model):
        self.request = request
        self.model = model

    def get_templates(self):
        model_name = self.model.__name__
        action_name = self.__class__.__name__
        templates = []
        if self.template:
            templates.append(self.template)
        model_template = "{0}_{1}_action.html".format(model_name, action_name)
        base_template = "public/object_action.html"
        templates.extend([model_template, base_template])
        return templates

    def get_fields(self):
        field_list = []
        for field in self.fields:
            name = field[0]
            f = field[1]
            formfield = f.formfield()
            field_list.append((name, formfield))
        field_dict = OrderedDict(field_list)
        return field_dict

    def get_form(self):
        fields = self.get_fields()
        form = type("ActionForm", (BaseForm, ), dict(base_fields=fields))
        return form

    def action_get_deal(self):
        form = self.get_form()
        context = dict(form=form(), help_text=self.help_text or self.verbose_name)
        templates = self.get_templates()
        return render(self.request, templates, context)

    def action_post_deal(self):
        try:
            form = self.get_form()(self.request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                self.action(**cleaned_data)
                response = "{0}".format(_(u"Operate successfully."))
                return HttpResponse(mark_safe(json.dumps({'ret': 'success', 'message': response})))
            else:
                message = {f: e.get_json_data(False) for f, e in form.errors.items()}
                self.response_error(message)
        except Exception, e:
            self.response_error("{0}".format(e))

    def action_view(self):
        request = self.request
        if request.method == "POST":
            return self.action_post_deal()
        if request.method == "GET":
            return self.action_get_deal()

    def get_objects(self):
        pk = self.request.POST.get('key', 'id')
        values = self.request.POST.getlist(pk)
        query_key = "{0}__in".format(pk)
        objects = self.model.objects.filter(**{query_key: values})
        return objects

    def response_error(self, message):
        response = {'ret': 'failed', 'message': message}
        return HttpResponse(mark_safe(json.dumps(response)))

    def action(self):
        raise NotImplementedError


class BaseModelAction(BaseAction):
    """
    The bath action of model that needn't to select the object(s).
    """
    model_action = True


class BaseObjAction(BaseAction):
    """
    The action of object that need to select the object(s).
    """
    object_action = True