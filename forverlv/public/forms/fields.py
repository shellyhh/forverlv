# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from django import forms
from django.forms.models import ChoiceField, ModelChoiceIterator


class TreeModelChoiceIterator(ModelChoiceIterator):

    def choice(self, obj):
        return (self.field.prepare_value(obj),
                self.field.prepare_parent_value(obj),
                self.field.label_from_instance(obj))


class TreeChoiceField(forms.ModelChoiceField):

    def __init__(self, queryset, empty_label=None, cache_choices=None,
                 required=True, widget=None, label=None, initial=None,
                 help_text='', to_field_name=None, limit_choices_to=None,
                 *args, **kwargs):
        self.parent_field = kwargs.pop('parent_field', None)
        super(TreeChoiceField, self).__init__(queryset, empty_label, cache_choices, required,
                                              widget, label, initial, help_text, to_field_name,
                                              limit_choices_to, *args, **kwargs)

    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return TreeModelChoiceIterator(self)

    choices = property(_get_choices, ChoiceField._set_choices)

    def prepare_parent_value(self, value):
        if hasattr(value, '_meta'):
            if self.parent_field:
                return value.serializable_value(self.parent_field) or 0
        return 0
