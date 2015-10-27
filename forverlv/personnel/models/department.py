# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from django.utils.translation import ugettext_lazy as _
from django.db import models
from public.base import BaseModel
from personnel.models.department_fields import DepartmentForeignKey


class Department(BaseModel):

    number = models.CharField(verbose_name=_(u'Department Number'), max_length=30, unique=True)
    name = models.CharField(verbose_name=_(u'Department Name'), max_length=30)
    parent_department = DepartmentForeignKey('self', verbose_name=_(u'Parent Department'),
                                             blank=True, null=True, related_name='children')

    def __init__(self, *args, **kwargs):
        super(Department, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return "{0} {1}".format(self.number, self.name)

    __repr__ = __str__

    class Admin(BaseModel.Admin):
        list_display = ('number', 'name', 'parent_department')
        actions = []

    class Meta:
        app_label = 'personnel'
        verbose_name = _(u'Department')
        verbose_name_plural = verbose_name

    def delete(self, using=None):
        if self.children.all().count() > 0:
            raise Exception(_(u"Can not delete department with there are children department."))
        super(Department, self).delete()
