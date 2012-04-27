from urlparse import parse_qs

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext as _

import gdata.auth
import gdata.photos.service

from picasa.async import async_fetch_albums

def _get_request_token(request):
    picasa_service = gdata.photos.service.PhotosService()
    picasa_service.SetOAuthInputParameters(gdata.auth.OAuthSignatureMethod.RSA_SHA1, settings.OAUTH_CONSUMER_KEY,
        rsa_key=settings.OAUTH_RSA_KEY)
    request_token = picasa_service.FetchOAuthRequestToken(settings.PICASA_SCOPES)
    picasa_service.SetOAuthToken(request_token)

    return picasa_service, request_token


@login_required
def login(request):
    if request.method != 'POST':
        return redirect('management:index')

    callback_url = request.build_absolute_uri(reverse('personal:oauth_endpoint'))

    picasa_service, request_token = _get_request_token(request)
    authorization_url = picasa_service.GenerateOAuthAuthorizationURL(callback_url=callback_url)

    return redirect(authorization_url)

@login_required
def endpoint(request):
    absolute_url = request.build_absolute_uri()

    picasa_service, request_token = _get_request_token(request)

    oauth_token = gdata.auth.OAuthTokenFromUrl(absolute_url)
    if oauth_token:
        oauth_token.oauth_input_params = gdata.auth.OAuthInputParams(gdata.auth.OAuthSignatureMethod.RSA_SHA1,
            settings.OAUTH_CONSUMER_KEY, rsa_key=settings.OAUTH_RSA_KEY)

        picasa_service.SetOAuthToken(oauth_token)
        access_token = picasa_service.UpgradeToOAuthAccessToken()

        token_string = access_token.get_token_string()
        token_string_data = parse_qs(token_string)

        profile = request.user.get_profile()
        profile.oauth_token = token_string_data['oauth_token'][0]
        profile.oauth_token_secret = token_string_data['oauth_token_secret'][0]
        profile.is_valid_token = True
        profile.save()

        async_fetch_albums.delay()
        messages.add_message(request, messages.INFO, _(u'Your photoalbums have been scheduled to be imported soon.'))

    return redirect('management:index')
