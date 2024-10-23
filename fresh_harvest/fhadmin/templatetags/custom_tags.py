from django import template
import os

register = template.Library()

@register.simple_tag
def list_files_js(directory):
    print(directory)
    js_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.js'):
                js_files.append(os.path.relpath(os.path.join(root, file), directory))
    return js_files


@register.simple_tag
def list_files_css(directory):
    print(directory)
    css_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.css'):
                css_files.append(os.path.relpath(os.path.join(root, file), directory))
    return css_files
