from itertools import groupby

from django.template import Library

register = Library()

@register.filter
def group(iterable, count):
    for groupper, values in groupby(enumerate(iterable), lambda (g, v): g // count):
        yield [v for i, v in values]
