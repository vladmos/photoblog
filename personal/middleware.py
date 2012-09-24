from django.utils import translation
from models import UserProfile

class LocaleMiddleware:
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            language_code = request.user.get_profile().language
        except AttributeError:
            return
        translation.activate(language_code)
        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        if 'Content-Language' not in response:
            response['Content-Language'] = translation.get_language()
        translation.deactivate()
        return response


class HostnameRoutingMiddleware:
    def process_request(self, request):
        hostname = request.META.get('HTTP_HOST')
        if ':' in hostname:
            hostname = hostname[:hostname.index(':')]

        try:
            request.owner = UserProfile.objects.get(custom_hostname__iexact=hostname).user
        except UserProfile.DoesNotExist:
            request.owner = None
