import gdata.auth
import gdata.photos.service
from gdata.photos.service import GooglePhotosException

from django.contrib.auth.models import User

from models import PicasaAlbum, PicasaPhoto

def _populate_photo(picasa_album, photo):
    try:
        picasa_photo = PicasaPhoto.objects.get(picasa_id=photo.gphoto_id.text)
    except PicasaPhoto.DoesNotExist:
        picasa_photo = PicasaPhoto(picasa_id=photo.gphoto_id.text)

    picasa_photo.album = picasa_album
    picasa_photo.page_url = photo.link[1].href
    picasa_photo.photo_url = photo.media.content[0].url
    picasa_photo.thumbnail_url = photo.media.thumbnail[1].url
    picasa_photo.description = photo.summary.text
    picasa_photo.save()

def _populate_album(picasa_service, user, album):
    try:
        picasa_album = PicasaAlbum.objects.get(picasa_id=album.gphoto_id.text)
    except PicasaAlbum.DoesNotExist:
        picasa_album = PicasaAlbum(picasa_id=album.gphoto_id.text)

    picasa_album.user = user
    picasa_album.name = album.name.text
    picasa_album.is_public = (album.access.text == 'public')
    picasa_album.save()

    photos_uri = album.GetPhotosUri()
    photos = picasa_service.GetFeed(photos_uri)
    for photo in photos.entry:
        _populate_photo(picasa_album, photo)

def fetch_albums():
    for user in User.objects.filter(profile__oauth_token__isnull=False):
        user_profile = user.get_profile()
        token_string = user_profile.oauth_token

        token = gdata.auth.AuthSubToken()
        token.set_token_string(token_string)

        picasa_service = gdata.photos.service.PhotosService()
        picasa_service.SetOAuthToken(token)

        try:
            albums = picasa_service.GetUserFeed()

            for album in albums.entry:
                _populate_album(picasa_service, user, album)

        except GooglePhotosException:
            user.profile.is_valid_token = False
            user.profile.save()