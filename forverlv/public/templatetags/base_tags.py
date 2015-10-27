# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from django import template
register = template.Library()
@register.filter
def bootstrap_field(field):
    html = """
    <div class="form-group" title="{help_text}">
        <label for="{id_for_label}" class="col-sm-2 control-label">{label}</label>
        <div class="col-sm-6">
            {field}
        </div>
    </div>
    """.format(**dict(help_text=field.help_text, id_for_label=field.id_for_label,
                      label=field.label, field=field.field))
    return html