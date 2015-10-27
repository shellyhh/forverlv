# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _


class UsernameInput(widgets.TextInput):

    def render(self, name, value, attrs=None):
        new_attrs = {
            'class': 'form-control',
            'placeholder': _(u'Username')
        }
        if attrs is None:
            attrs = new_attrs
        else:
            attrs.update(new_attrs)
        return super(UsernameInput, self).render(name, value, attrs)


class PasswordInput(widgets.PasswordInput):

    def render(self, name, value, attrs=None):
        new_attrs = {
            'class': 'form-control',
            'placeholder': _(u'Password')
        }
        if attrs is None:
            attrs = new_attrs
        else:
            attrs.update(new_attrs)
        return super(PasswordInput, self).render(name, value, attrs)