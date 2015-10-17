from django import template

register = template.Library()


@register.simple_tag
def active_func(section):
    section_pattern = [
            'version',
            'project',
            'user',
            ]
    if section in section_pattern: return "class='open'"



