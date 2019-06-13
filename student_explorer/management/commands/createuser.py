from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
# from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = 'Adds a user with an unusable password'

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='+', type=str)

    def handle(self, *args, **options):
        User = get_user_model()
        for username in options['username']:
            try:
                user = User.objects.create_user(username, password=None)
            except Exception as e:
                raise CommandError(
                    'User "%s" could not be created ("%s")' % (username, e))
            # user.set_unusable_password()
            # user.save()

            self.stdout.write(self.style.SUCCESS(
                'Created user "%s"' % user.username))
