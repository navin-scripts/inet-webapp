from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "scripts to interact with rtr30"

    def add_arguments(self, parser):
        parser.add_argument("--get-tunnels",action="store_true",help="Populate UnifiSite Model")
    
    def handle(self, *args, **options):
        if options['get-tunnels']:
            pass