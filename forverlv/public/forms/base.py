# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from django.db import models
from django.utils.translation import ugettext_lazy as _
from public.forms.fields import TreeChoiceField
from public.forms.widgets import ObjectSingleSelect


class ObjectForeignKey(models.ForeignKey):

    form_class = TreeChoiceField
    widget = ObjectSingleSelect
    parent_field = None

    def __init__(self, *args, **kwargs):
        if self.parent_field is None:
            raise Exception(_(u"The attribute parent_field can't be None."))
        super(ObjectForeignKey, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': self.form_class,
            'widget': self.widget,
            'parent_field': self.parent_field
        }
        defaults.update(kwargs)
        return super(ObjectForeignKey, self).formfield(**defaults)