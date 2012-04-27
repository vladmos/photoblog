import gdata.auth
import gdata.photos.service
from gdata.photos.service import GooglePhotosException

from django.contrib.auth.models import User
from django.conf import settings

from models import PicasaAlbum, PicasaPhoto

def _update_photos(picasa_album, photos):
    picasa_photos = PicasaPhoto.objects.filter(album=picasa_album)
    obsolete_picasa_photos_id = set(p.id for p in picasa_photos)

    for photo in photos.entry:

        try:
            picasa_photo = PicasaPhoto.objects.get(picasa_id=photo.gphoto_id.text)
            obsolete_picasa_photos_id.remove(picasa_photo.id)
        except PicasaPhoto.DoesNotExist:
            picasa_photo = PicasaPhoto(picasa_id=photo.gphoto_id.text)

        picasa_photo.album = picasa_album
        picasa_photo.page_url = photo.link[1].href
        picasa_photo.photo_url = photo.media.content[0].url
        picasa_photo.thumbnail_url = photo.media.thumbnail[1].url
        picasa_photo.description = photo.summary.text
        picasa_photo.width = int(photo.width.text)
        picasa_photo.height = int(photo.height.text)
        picasa_photo.save()

    PicasaPhoto.objects.filter(id__in=obsolete_picasa_photos_id).delete()

def _update_albums(picasa_service, user, albums):
    picasa_albums = PicasaAlbum.objects.filter(user=user)
    obsolete_picasa_albums_id = set(a.id for a in picasa_albums)

    for album in albums.entry:

        try:
            picasa_album = PicasaAlbum.objects.get(picasa_id=album.gphoto_id.text)
            obsolete_picasa_albums_id.remove(picasa_album.id)
        except PicasaAlbum.DoesNotExist:
            picasa_album = PicasaAlbum(picasa_id=album.gphoto_id.text)

        picasa_album.user = user
        picasa_album.name = album.title.text
        picasa_album.access_type = album.access.text
        picasa_album.album_url = album.link[1].href
        picasa_album.save()

        photos_uri = album.GetPhotosUri()
        photos = picasa_service.GetFeed(photos_uri)
        _update_photos(picasa_album, photos)

    PicasaAlbum.objects.filter(id__in=obsolete_picasa_albums_id).delete()

def fetch_albums():
    for user in User.objects.filter(profile__is_valid_token=True):
        user_profile = user.get_profile()

        oauth_token = gdata.auth.OAuthToken(key=user_profile.oauth_token,
            secret=user_profile.oauth_token_secret, scopes=settings.PICASA_SCOPES)
        oauth_token.oauth_input_params = gdata.auth.OAuthInputParams(gdata.auth.OAuthSignatureMethod.RSA_SHA1,
            settings.OAUTH_CONSUMER_KEY, rsa_key=settings.OAUTH_RSA_KEY)

        picasa_service = gdata.photos.service.PhotosService()
        picasa_service.SetOAuthInputParameters(gdata.auth.OAuthSignatureMethod.RSA_SHA1, settings.OAUTH_CONSUMER_KEY,
            rsa_key=settings.OAUTH_RSA_KEY)

        picasa_service.SetOAuthToken(oauth_token)

        try:
            albums = picasa_service.GetUserFeed()
            _update_albums(picasa_service, user, albums)

        except GooglePhotosException, e:
            user_profile.is_valid_token = False
            user_profile.save()
            pass