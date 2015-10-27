# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from django.utils.safestring import mark_safe
from django.http import HttpResponse
import json
from public.utils import StrJSONEncoder


class ChangelistView(object):

    def __init__(self, request, model):
        self.request = request
        self.model = model
        self.model_admin = model.Admin
        self.list_display = model.Admin.list_display
        self.lookup_opts = model._meta
        self.pk_attname = model._meta.pk.attname
        if self.pk_attname not in self.list_display:
            self.list_display += (self.pk_attname, )

    def _get_default_ordering(self):
        ordering = []
        if self.model_admin.ordering:
            ordering = self.model_admin.ordering
        elif self.lookup_opts.ordering:
            ordering = self.lookup_opts.ordering
        return ordering

    def get_queryset(self):
        queryset = self.model._default_manager.get_queryset()
        return queryset

    def changelist_view(self):
        qs = self.get_queryset()
        results = qs.values(*self.list_display)
        grid_context = dict(data=results)
        return HttpResponse(mark_safe(json.dumps(grid_context, cls=StrJSONEncoder)))
