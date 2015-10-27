# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from django.forms.widgets import SelectMultiple
# from django.contrib.auth.models import Permission
# from django.conf import settings
from public.constant import SYSTEM_APPS
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_text, force_str
from django.forms.utils import flatatt
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.template import loader
import json


class PermissionSelectMultiple(SelectMultiple):

    def __init__(self, attrs=None, choices=()):
        self.display = ''
        self.app_base = 1000
        self.model_base = 2000
        super(PermissionSelectMultiple, self).__init__(attrs, choices)

    def render(self, name, value, attrs=None, choices=()):
        cts = ContentType.objects.all()
        tree = [dict(id=self.app_base+index, pId=0, name=force_str(app), checked='false', open='true') for index, app in enumerate(SYSTEM_APPS)]
        for index, ct in enumerate(cts):
            if ct.app_label in SYSTEM_APPS:
                model_id = self.model_base + index
                tree.append(dict(id=model_id, pId=SYSTEM_APPS.index(ct.app_label)+self.app_base,
                                 name=force_str(ct.model), checked='false'))
                model_permissions = ct.permission_set.all()
                for mp in model_permissions:
                    tree.append(dict(id=mp.id, pId=model_id,
                                     name=force_str(mp.name), checked='false'))
        final_attrs = self.build_attrs(attrs, name=name, value=value, type='hidden')
        display_attrs = {
            'id': "display_{0}".format(name),
            'class': 'form-control',
            'value': self.display
        }
        output = """
        <input {attrs} />
        <div id="down_{name}" class="input-group" style="display:none">
            <input {display_attrs}>
            <div class="input-group-addon"><i class="glyphicon glyphicon-chevron-down"></i></div>
        </div>
        <div id="zTree_{name}" class="zTreeBackground left">
            <ul id="tree_{name}" class="ztree"></ul>
        </div>
        {script}
        """
        script = loader.render_to_string('group_tree.html',
                                         {'nodes': mark_safe(json.dumps(tree)), 'name': name, 'toggle': 'false'})
        return format_html(output, attrs=flatatt(final_attrs), display_attrs=flatatt(display_attrs),
                           name=force_text(name), script=mark_safe(script))