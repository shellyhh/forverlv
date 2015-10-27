# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from public.forms.base import ObjectForeignKey


class PositionForeignKey(ObjectForeignKey):

    parent_field = 'parent_position'

    def __init__(self, *args, **kwargs):
        super(PositionForeignKey, self).__init__(*args, **kwargs)



