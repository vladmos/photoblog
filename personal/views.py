from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext as _

import gdata.auth
import gdata.photos.service
from gdata.service import NonAuthSubToken

from picasa.async import async_fetch_albums

@login_required
def login(request):
    if request.method != 'POST':
        return redirect('management:index')

    next = request.build_absolute_uri(reverse('personal:oauth_endpoint'))
    scope = ' '.join(settings.PICASA_SCOPES)
    secure = False  # set secure=True to request secure AuthSub tokens
    session = True
    auth_sub_url = gdata.auth.GenerateAuthSubUrl(next, scope, secure=secure, session=session)
    return redirect(auth_sub_url)

@login_required
def endpoint(request):
    absolute_url = request.build_absolute_uri()

    single_use_token = gdata.auth.extract_auth_sub_token_from_url(absolute_url)
    picasa_service = gdata.photos.service.PhotosService()

    try:
        picasa_service.UpgradeToSessionToken(single_use_token)
    except NonAuthSubToken:
        pass
    else:
        token_store =  picasa_service.token_store
        token = token_store.find_token(settings.PICASA_SCOPES[0])
        token_string = token.get_token_string()

        profile = request.user.get_profile()
        profile.oauth_token = token_string
        profile.is_valid_token = True
        profile.save()

        async_fetch_albums.delay()
        messages.add_message(request, messages.INFO, _(u'Your photoalbums have been scheduled to be imported soon.'))

    return redirect('management:index')
