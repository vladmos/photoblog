from django.utils import translation

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
