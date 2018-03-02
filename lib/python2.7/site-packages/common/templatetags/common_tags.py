# -*- coding: utf-8
"""
Template tags:
 * alter_qs - allows to modify arguement in URL query string
 * set - allows to set new variable in template

Credits:
 * code for `set` tag is based on http://djangosnippets.org/snippets/215/
"""
from cgi import parse_qsl
from urllib import urlencode

from django import template
from django.utils.encoding import smart_str


register = template.Library()

@register.simple_tag
def alter_qs(qs, name, value, name2=None, value2=None):
    """
    Alter query string argument with new value.

    Usage in template:
        <a href="/foo/bar{% alter_qs request.META.QUERY_STRING "page" 3 %}">Some link</a>

    Usage in code:
        from common.templatetags.common_tags import alter_qs
        url = alter_qs(some_url, "page", "4")
    """

    qs = qs.lstrip('?')
    args = [[x[0], smart_str(x[1])] for x in parse_qsl(qs, keep_blank_values=True)]
    if value:
        found = False
        for arg in args:
            if arg[0] == name:
                arg[1] = smart_str(value)
                found = True
        if not found:
            args.append([name, smart_str(value)])
    else:
        args = [x for x in args if x[0] != name]
    if args:
        args = [tuple(x) for x in args]
        result = '?' + urlencode(args)
        if name2 and value2:
            return alter_qs(result, name2, value2)
        else:
            return result
    else:
        return ''



@register.tag(name='set')
def do_set_varable(parser,token):
    """
    Set new value in the context of template.

    Usage:
        {% set category_list category.categories.all %}
        {% set dir_url "../" %}
        {% set type_list "table" %}
        {% include "category_list.html" %}
    """
    from re import split
    bits = split(r'\s+', token.contents, 2)
    return SetVariableNode(bits[1],bits[2])


class SetVariableNode(template.Node):
    """
    Template Node of `set` tag.
    """

    def __init__(self,varname,value):
        self.varname = varname
        self.value = value
    
    def render(self,context):
        var = template.resolve_variable(self.value,context)
        if var:
            context[self.varname] = var
        else:
            context[self.varname] = context[self.value]
        return ''
