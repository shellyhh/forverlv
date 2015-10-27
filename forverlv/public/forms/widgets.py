# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from django import forms
from django.utils.encoding import force_text, force_str
# from django.utils.translation import ugettext_lazy as _
from django.forms.utils import flatatt
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.template import loader
import json


class PublicTextInputWidget(forms.TextInput):

    def render(self, name, value, attrs=None):
        if attrs:
            attrs.update({'class': 'form-control'})
        else:
            attrs = {'class': 'form-control'}
        return super(PublicTextInputWidget, self).render(name, value, attrs)


class PublicForeignKeyWidget(forms.Select):

    def render(self, name, value, attrs=None, choices=()):
        if attrs:
            attrs.update({'class': 'form-control'})
        else:
            attrs = {'class': 'form-control'}
        return super(PublicForeignKeyWidget, self).render(name, value, attrs, choices)


class ObjectSingleSelect(forms.Select):

    def __init__(self, attrs=None, choices=()):
        self.display = ''
        super(ObjectSingleSelect, self).__init__(attrs, choices)

    def _node_wrapper(self, obj, parent, label, value):
        if obj == value:
            checked = 'true'
            self.display = force_str(label)
        else:
            checked = 'false'
        return dict(id=obj, pId=parent, name=force_str(label), checked=force_str(checked))

    def _nodes_wrapper(self, value):
        nodes = []
        for obj_id, parent_id, label in self.choices:
            nodes.append(self._node_wrapper(obj_id, parent_id, label, value))
        return nodes

    def get_nodes(self, value):
        return self._nodes_wrapper(value)

    def render(self, name, value, attrs=None, choices=()):
        nodes = self.get_nodes(value)
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name, value=value, type='hidden')
        display_attrs = {
            'id': "display_{0}".format(name),
            'class': 'form-control',
            'value': self.display
        }
        output = """
        <input {attrs} />
        <div id="down_{name}" class="input-group">
            <input {display_attrs}>
            <div class="input-group-addon"><i class="glyphicon glyphicon-chevron-down"></i></div>
        </div>
        <div id="zTree_{name}" class="zTreeBackground left" style="display:none">
            <ul id="tree_{name}" class="ztree"></ul>
        </div>
        {script}
        """
        script = loader.render_to_string('public/object_tree.html',
                                         {'nodes': mark_safe(json.dumps(nodes)), 'name': name})
        return format_html(output, attrs=flatatt(final_attrs), display_attrs=flatatt(display_attrs),
                           name=force_text(name), script=mark_safe(script))


