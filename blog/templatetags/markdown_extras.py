# blog/templatetags/markdown_extras.py
from django import template
from django.template.defaultfilters import stringfilter
from markdownx.utils import markdownify

register = template.Library()


@register.filter()
@stringfilter
def markdown(value):
    """Renderuje MarkdownxField"""
    return markdownify(value)