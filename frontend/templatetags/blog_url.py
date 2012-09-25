from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def blog_url(user):
    return u'http://%s%s' % (
        user.profile.custom_hostname,
        reverse('frontend:blog'),
    )

@register.simple_tag
def blog_rss_url(user):
    return u'http://%s%s' % (
        user.profile.custom_hostname,
        reverse('frontend:rss'),
    )

@register.simple_tag
def article_url(user, article):
    return u'http://%s%s' % (
        user.profile.custom_hostname,
        article.get_absolute_url(),
    )

