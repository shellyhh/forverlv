# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from django.db import models
from django.contrib import admin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from public.constant import STATUS_OK, STATUS_STOP
from public.action.actions import default_actions
Meta = type(models.Model)


class BaseMeta(Meta):

    def __new__(cls, name, bases, attrs):
        base_actions = []
        tmp = (base for base in bases if getattr(base, 'Admin', None))
        for base in tmp:
            base_actions.extend(getattr(base.Admin, 'actions', []))
        base_actions.extend(getattr(attrs['Admin'], 'actions', []))
        attr_meta = attrs.get('Meta', None)
        abstract = getattr(attr_meta, 'abstract', False)
        actions_dict = {}
        extra_permission = ()
        for action in base_actions:
            actions_dict[action.__name__] = action
            if not abstract:
                permission_name = "Can {0} {1}".format(action.__name__, name)
                codename = "{0}_{1}".format(action.__name__, name).lower()
                extra_permission += ((codename, permission_name), )
        if attr_meta:
            #change default permissions
            setattr(attr_meta, 'default_permissions', ('browser', 'add', 'change', 'delete'))
            #add action permissions
            setattr(attr_meta, 'permissions', extra_permission)
        attrs.update({'Meta': attr_meta, 'actions': actions_dict})
        new_cls = Meta.__new__(cls, name, bases, attrs)
        return new_cls


class BaseModel(models.Model):

    create_time = models.DateTimeField(verbose_name=_(u'Create Time'), default=timezone.now, editable=False, blank=True, null=True)
    delete_time = models.DateTimeField(verbose_name=_(u'Delete Time'), editable=False, blank=True, null=True)
    update_time = models.DateTimeField(verbose_name=_(u'Update Time'), editable=False, blank=True, null=True)
    create_user = models.CharField(verbose_name=_(u'Create User'), max_length=30, editable=False, blank=True, null=True)
    delete_user = models.CharField(verbose_name=_(u'Delete User'), max_length=30, editable=False, blank=True, null=True)
    update_user = models.CharField(verbose_name=_(u'Update User'), max_length=30, editable=False, blank=True, null=True)
    obj_status = models.SmallIntegerField(verbose_name=_(u'Object Status'), default=STATUS_OK, editable=False, blank=True, null=True)
    __metaclass__ = BaseMeta

    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)

    @classmethod
    def get_action(cls, action_name):
        actions = getattr(cls, 'actions', {})
        return actions.get(action_name, None)

    class Admin(admin.ModelAdmin):
        actions = default_actions
        creation_form = None
        change_form = None

    class Meta:
        abstract = True

