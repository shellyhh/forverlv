# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from public.forms.base import ObjectForeignKey


class DepartmentForeignKey(ObjectForeignKey):

    parent_field = 'parent_department'

    def __init__(self, *args, **kwargs):
        super(DepartmentForeignKey, self).__init__(*args, **kwargs)
