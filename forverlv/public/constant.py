# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from django.db import models
from django.conf import settings
from public.forms import widgets
# from django import forms
STATUS_OK = 0
STATUS_STOP = 1
FORMFIELD_FOR_DBFIELD_DEFAULTS = {
    # models.DateTimeField: {
    #     'form_class': forms.SplitDateTimeField,
    #     'widget': widgets.AdminSplitDateTime
    # },
    # models.DateField: {'widget': widgets.AdminDateWidget},
    # models.TimeField: {'widget': widgets.AdminTimeWidget},
    # models.TextField: {'widget': widgets.AdminTextareaWidget},
    # models.URLField: {'widget': widgets.AdminURLFieldWidget},
    # models.IntegerField: {'widget': widgets.AdminIntegerFieldWidget},
    # models.BigIntegerField: {'widget': widgets.AdminBigIntegerFieldWidget},
    models.CharField: widgets.PublicTextInputWidget,
    # models.ImageField: {'widget': widgets.AdminFileWidget},
    # models.FileField: {'widget': widgets.AdminFileWidget},
    # models.EmailField: {'widget': widgets.AdminEmailInputWidget},
    models.ForeignKey: widgets.PublicForeignKeyWidget
}
SYSTEM_APPS = [app for app in settings.INSTALLED_APPS if app not in settings.IGNORE_APPS]
EXTRA_PERMISSIONS =(

)