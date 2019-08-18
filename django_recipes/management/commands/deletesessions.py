from django.contrib.sessions.models import Session
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help =  "Companion management command to clearsessions"

    def handle(self, **options):
        # https://docs.djangoproject.com/en/stable/topics/auth/customizing/#specifying-authentication-backends
        sessions_deleted, _ = Session.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Removed %i user sessions." % sessions_deleted))
