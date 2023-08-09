from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "scripts to interact with unifi"

    def add_arguments(self, parser):
        parser.add_argument(
            "--kit",
            action="store_true",
            help="Populate Kit Model",
        )
        parser.add_argument(
            "--unifi",
            action="store_true",
            help="Populate UniFi Models",
        )
        parser.add_argument(
            "--meraki",
            action="store_true",
            help="Populate Meraki Models",
        )
        parser.add_argument(
            "--bec",
            action="store_true",
            help="Populate BEC Models",
        )


    def handle(self, *args, **options):
        if options['unifi']:
            from .vendors.unifi import PopulateUniFi
            e = PopulateUniFi()
            sites = e.sitePopulater()
            self.stdout.write(
                self.style.SUCCESS('Successfully populated sites: %s' % sites)
            )
            devices = e.devices()
            self.stdout.write(
                self.style.SUCCESS('Successfully populated devices: %s' % devices)
            )
        if options['meraki']:
            from .vendors.meraki import populateMerakis
            count_of_merakis = 0
            merakis = populateMerakis()
            for meraki in merakis:
                for m in meraki:
                    if m['serial']:
                        count_of_merakis += 1
            self.stdout.write(
                self.style.SUCCESS('Successfully populated merakis: %s' % count_of_merakis)
            )
        if options['bec']:
            from .vendors.bec import becentral
            becs = becentral()
            self.stdout.write(
                self.style.SUCCESS('Successfully populated BECs: %s' % becs)
            )
        if options['kit']:
            self.stdout.write(self.style.WARNING("Attempting to populate the database..."))
            from .vendors.unifi import PopulateUniFi
            from .vendors.meraki import populateMerakis
            from .vendors.bec import becentral
            from .vendors.kit import populateKits
            becs = becentral() # Get BECs from BECentral
            self.stdout.write(self.style.SUCCESS('Successfully populated becs from BECentral: %s' % becs))
            merakis = populateMerakis() # Get Merakis from Meraki Dashboard
            self.stdout.write(self.style.SUCCESS('Successfully populated meraki devices: %s' % merakis))
            e = PopulateUniFi() # Initialize UniFi
            sites = e.sitePopulater() # Get Sites from the UniFi Controller
            self.stdout.write(self.style.SUCCESS('Successfully populated unifi sites: %s' % sites))
            devices = e.devices() # Get Devices from the UniFi Controller
            self.stdout.write(self.style.SUCCESS('Successfully populated devices: %s' % devices))
            bec_clients = e.clients() # Get BEC clients from the UniFi Controller
            self.stdout.write(self.style.SUCCESS('Successfully populated unifi bec clients: %s' % bec_clients))
            kits = populateKits()
            self.stdout.write(self.style.SUCCESS('Successfully populated the kit database: %s' %kits))
        