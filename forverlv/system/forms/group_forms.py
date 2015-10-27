# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from django import forms
from django.utils.translation import ugettext_lazy as _
from system.models import Group
from system.forms.widgets import PermissionSelectMultiple


class GroupCreationFrom(forms.ModelForm):

    permissions1 = forms.ModelMultipleChoiceField(queryset=None,
                                                  label=_("Permissions"), widget=PermissionSelectMultiple)

    class Meta:
        model = Group
        fields = ('name', )