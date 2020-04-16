from django.core.management.base import BaseCommand, CommandError

from management import import_fixtures

class Command(BaseCommand):
    help = 'Imports fixture data for the management application'

    def handle(self, *args, **options):
        try:
            import_fixtures.main()
            self.stdout.write(self.style.SUCCESS('Import of management fixtures succeeded'))
        except Exception:
            raise CommandError('Import of management fixtures failed')

