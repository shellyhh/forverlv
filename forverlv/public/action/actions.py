# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from public.action.base import BaseModelAction, BaseObjAction
from django.utils.translation import ugettext_lazy as _
__all__ = ['default_actions']


class ModelAdd(BaseModelAction):
    verbose_name = _(u"Addition")

    def action(self):
        pass


class ModelDelete(BaseObjAction):
    verbose_name = _(u"Delete")
    help_text = _(u"Are you want to delete the selected object(s)?")

    def action(self):
        objects = self.get_objects()
        for obj in objects:
            obj.delete()


class ModelEdit(BaseObjAction):
    verbose_name = _(u"Edit")

    def action(self):
        pass

default_actions = [ModelAdd, ModelDelete, ModelEdit]


