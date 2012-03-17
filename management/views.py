from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect

from utils import response
from picasa.models import PicasaAlbum

@login_required
def index(request):
    return response(request, 'index.html', {
        'google_token_management_url': settings.GOOGLE_TOKEN_MANAGEMENT_URL,
    })

@login_required
def photoalbum(request, photoalbum_id):
    album = get_object_or_404(PicasaAlbum, id=photoalbum_id)

    if album.user.id != request.user.id:
        return redirect('management:photoalbums')

    return response(request, 'photoalbum.html', {
        'photoalbum': album,
    })

@login_required
def photoalbums(request):
    return response(request, 'photoalbums.html')
