# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from django.db import models
from django.utils.translation import ugettext_lazy as _
from public.base import BaseModel
from personnel.models.department import Department
from personnel.models.department_fields import DepartmentForeignKey
from personnel.models.position_fields import PositionForeignKey


class Position(BaseModel):

    number = models.CharField(verbose_name=_(u'Position Number'), max_length=30, unique=True, blank=False, null=False)
    name = models.CharField(verbose_name=_(u'Position Name'), max_length=30)
    parent_position = PositionForeignKey('self', verbose_name=_(u'Parent Position'), blank=True, null=True)
    department = DepartmentForeignKey(Department, verbose_name=_(u'Department'))

    def __init__(self, *args, **kwargs):
        super(Position, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return "{0} {1}".format(self.number, self.name)

    __repr__ = __str__

    class Admin(BaseModel.Admin):
        list_display = ('number', 'name', 'parent_position', 'department')
        actions = []

    class Meta:
        app_label = 'personnel'
        verbose_name = _(u'Position')
        verbose_name_plural = verbose_name