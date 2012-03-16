from django.contrib.auth.decorators import login_required
from django.conf import settings

from utils import response

@login_required
def index(request):
    return response(request, 'index.html', {
        'google_token_management_url': settings.GOOGLE_TOKEN_MANAGEMENT_URL,
    })