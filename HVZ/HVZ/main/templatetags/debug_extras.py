from django.template import Library

register = Library()


@register.filter
def do_dir(thing):
    return dir(thing)
