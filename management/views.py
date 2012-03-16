from django.contrib.auth.decorators import login_required
from django.conf import settings

from utils import response
from picasa.models import PicasaAlbum

@login_required
def index(request):
    my_albums = PicasaAlbum.objects.filter(user=request.user)
    return response(request, 'index.html', {
        'photoalbums': my_albums,
        'google_token_management_url': settings.GOOGLE_TOKEN_MANAGEMENT_URL,
    })