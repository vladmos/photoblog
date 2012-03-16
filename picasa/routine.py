import gdata.auth
import gdata.photos.service
from django.contrib.auth.models import User

from models import PicasaAlbum

def fetch_albums():
    for user in User.objects.filter(profile__oauth_token__isnull=False):
        user_profile = user.get_profile()
        token_string = user_profile.oauth_token

        token = gdata.auth.AuthSubToken()
        token.set_token_string(token_string)

        picasa_service = gdata.photos.service.PhotosService()
        picasa_service.SetOAuthToken(token)

        albums = picasa_service.GetUserFeed()

        for album in albums.entry:
            try:
                picasa_album = PicasaAlbum.objects.get(picasa_id=album.gphoto_id.text)
            except PicasaAlbum.DoesNotExist:
                picasa_album = PicasaAlbum(picasa_id=album.gphoto_id.text)
            picasa_album.user = user
            picasa_album.name = album.name.text
            picasa_album.is_public = (album.access.text == 'public')
            picasa_album.save()