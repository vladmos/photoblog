import pytz

from django import template
from django.utils.safestring import mark_safe
from django.conf import settings

register = template.Library()

def _utc_datetime(dt):
    local_timezone = pytz.timezone(settings.TIME_ZONE)
    utc_dt = local_timezone.localize(dt).astimezone(pytz.UTC)
    return utc_dt

@register.filter
def rss_datetime(dt):
    if not dt:
        return ''
    return _utc_datetime(dt).strftime('%a, %d %b %Y %H:%M:%S GMT')

@register.filter
def post_datetime(dt):
    return _utc_datetime(dt).strftime('%d %B %Y')