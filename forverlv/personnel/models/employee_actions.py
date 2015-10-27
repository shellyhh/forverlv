# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from public.action.base import BaseModelAction, BaseObjAction
from personnel.models.department_fields import DepartmentForeignKey
from personnel.models.department import Department
from django.utils.translation import ugettext_lazy as _


class AdjustDepartment(BaseObjAction):

    fields = (
        ('new_department', DepartmentForeignKey(Department, verbose_name=_(u'New Department'))),
    )

    def action(self, new_department):
        objs = self.get_objects()
        for obj in objs:
            obj.department = new_department
            obj.save()