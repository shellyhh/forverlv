# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from django.utils.translation import ugettext as _
from django.forms.models import ModelForm
from django.shortcuts import render
from django.http import HttpResponse
from itertools import chain
import json
from public.constant import FORMFIELD_FOR_DBFIELD_DEFAULTS


class ModelView(object):

    def __init__(self, request, model, object_id):
        self.request = request
        self.model = model
        self.admin = getattr(model, 'Admin', None)
        self.opts = model._meta
        self.object_id = object_id

    def get_object(self):
        obj = self.model.objects.get(pk=self.object_id)
        return obj

    def get_fields(self):
        fields = []
        widgets = {}
        for f in chain(self.opts.concrete_fields, self.opts. many_to_many):
            if not getattr(f, 'editable', False):
                continue
            fields.append(f.name)
            if f.__class__ in FORMFIELD_FOR_DBFIELD_DEFAULTS:
                widgets[f.name] = FORMFIELD_FOR_DBFIELD_DEFAULTS[f.__class__]
        return fields, widgets

    def form_factory(self):
        fields, widgets = self.get_fields()
        meta = type('Meta', (type,), {
            'model': self.model,
            'fields': fields,
            'widgets': widgets
        })
        form_name = "{0}{1}Form".format(self.opts.app_label, self.model.__name__)
        form = type(form_name, (ModelForm, ), {'Meta': meta})
        return form

    def get_from(self, request, obj):
        from django.forms import ModelForm
        from django.utils.module_loading import import_string
        form_type = 'change_form' if obj else 'creation_form'
        form = None
        if self.admin:
            form_path = getattr(self.admin, form_type)
            if form_path:
                form = import_string(form_path)
        if form and issubclass(form, ModelForm):
            return form
        else:
            return self.form_factory()

    def save_form(self, form, change):
        return form.save(commit=True)

    def response_model_view(self, add):
        if add:
            response = dict(ret='success', message=_('Save Successfully.'))
        else:
            response = dict(ret='success', message=_('Update Successfully.'))
        return HttpResponse(json.dumps(response))

    def response_error(self, message):
        response = dict(ret='failed', message=message)
        return HttpResponse(json.dumps(response))

    def get_templates(self):
        templates = []
        if self.object_id:
            base_template = 'public/object_action.html'
            model_template = '{0}_edit.html'.format(self.model.__class__.__name__)
        else:
            base_template = 'public/model_add.html'
            model_template = '{0}_add.html'.format(self.model.__class__.__name__)
        templates.extend([model_template, base_template])
        return templates

    def model_view(self):
        # print "[*]Model View."
        request = self.request
        model = self.model
        add = self.object_id is None
        if add:
            obj = None
        else:
            obj = self.get_object()

        MForm = self.get_from(request, obj)
        if request.method == "POST":
            form = MForm(data=request.POST, files=request.FILES, instance=obj)
            if form.is_valid():
                form_validated = True
                new_object = self.save_form(form, change=not add)
            else:
                form_validated = False
                new_object = form.instance
            if form_validated:
                return self.response_model_view(add)
            else:
                message = {f: e.get_json_data(False) for f, e in form.errors.items()}
                print message
                return self.response_error(message)
        else:
            if add:
                initial = {}
                form = MForm(initial=initial)
            else:
                form = MForm(instance=obj)
            context = dict(form=form)
            templates = self.get_templates()
            return render(request, templates, context)
