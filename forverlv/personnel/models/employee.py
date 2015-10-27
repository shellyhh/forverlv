# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from django.db import models
from django.utils.translation import ugettext_lazy as _
from personnel.models.department import Department
from personnel.models.position import Position
from public.base import BaseModel
from personnel.models.employee_actions import AdjustDepartment
from personnel.models.department_fields import DepartmentForeignKey
from personnel.models.position_fields import PositionForeignKey


class Employee(BaseModel):

    number = models.CharField(verbose_name=_(u'Employee Number'), max_length=30, unique=True, blank=False, null=False)
    first_name = models.CharField(verbose_name=_(u'First Name'), max_length=30,
                                  help_text=_(u'The first name'))
    last_name = models.CharField(verbose_name=_(u'Last Name'), max_length=30)
    department = DepartmentForeignKey(Department, verbose_name=_(u'Department'))
    position = PositionForeignKey(Position, verbose_name=_(u'Position'))

    def __init__(self, *args, **kwargs):
        super(Employee, self).__init__(*args, **kwargs)

    def __str__(self):
        return "{0} {1}".format(self.number, self.first_name)

    __repr__ = __str__

    class Admin(BaseModel.Admin):
        # list_display = ('number', 'first_name', 'last_name', 'department__name', 'position__name')
        list_display = ('number', 'first_name', 'last_name', 'department', 'position')
        actions = [AdjustDepartment]

    class Meta:
        app_label = 'personnel'
        verbose_name = _(u'Employee')
        verbose_name_plural = verbose_name

    def save(self, raw=False, force_insert=False,
             force_update=False, using=None, update_fields=None):
        super(Employee, self).save()

    def get_department_name(self):
        return self.department.name

    def get_position_name(self):
        return self.position.name
