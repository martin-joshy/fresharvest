from django import template
import os

register = template.Library()

@register.simple_tag
def list_files_js(directory):
    print(directory)
    return [f for f in os.listdir(directory) if f.endswith('.js')]


@register.simple_tag
def list_files_css(directory):
    print(directory)
    return [f for f in os.listdir(directory) if f.endswith('.css')]
