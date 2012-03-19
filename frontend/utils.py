import re
from functools import partial

from markdown2 import markdown
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

from picasa.models import PicasaPhoto

def response(request, template, context=None):
    context = context or {}
    return render_to_response(template, context, context_instance=RequestContext(request))

PHOTO_RE = re.compile(r'\[photo_(?P<photo_id>\d+)\]')

def _photo_tag(user, matching):
    photo_id = matching.group('photo_id')

    try:
        photo = PicasaPhoto.objects.get(id=photo_id, album__user=user)
    except PicasaPhoto.DoesNotExist:
        return u''

    url = photo.photo_url

    if photo.width >= settings.PHOTO_SIZE or photo.height >= settings.PHOTO_SIZE:
        last_slash_index = url.rfind('/')
        url = u'%s/s%s%s' % (url[:last_slash_index], settings.PHOTO_SIZE, url[last_slash_index:])

    return u'<img src="%s" />' % url

def compile_article(owner, text):
    text = markdown(text)

    insert_photo = partial(_photo_tag, owner)
    text = PHOTO_RE.sub(insert_photo, text)

    return text