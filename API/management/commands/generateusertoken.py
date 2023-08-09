from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "scripts to interact with api"

    def add_arguments(self, parser):
        parser.add_argument(
            "--api-user",
            action="store_true",
            help="Generate User Token",
        )

    def handle(self, *args, **options):

        if options['api_user']:
            from rest_framework.authtoken.models import Token
            from django.contrib.auth.models import User

            user = User.objects.get(username='navin')
            token, created = Token.objects.get_or_create(user=user)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created token for user: {user}: {token}')
            )
