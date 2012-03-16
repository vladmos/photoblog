from django.core.management.base import NoArgsCommand

from picasa.routine import fetch_albums

class Command(NoArgsCommand):
    help = 'Fetch albums and photos for all users with a token'

    def handle_noargs(self, **options):
        fetch_albums()