from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key
import os

class Command(BaseCommand):
    """
    Generate a Django secret key in `secretkey.txt` if none exists
    """
    args = 'secretkey.txt'
    help = 'Generate a Django secret key'
    can_import_settings = False
    leave_locale_alone = True

    # Where to create the key if no parameter is given
    # This will be monkey-patched when runnning the tests
    BASE_DIR = os.getcwd()

    def add_arguments(self, parser):
        parser.add_argument(
            '--replace',
            action='store_true',
            dest='replace',
            default=False,
            help='Replace the existing key'
        )

    def handle(self, *args, **options):

        if len(args) > 1:
            self.stderr.write("Please provide only one file name (or none).")
            return

        key_filename = args[0] if args else 'secretkey.txt'
        key_filepath = os.path.join(self.BASE_DIR, key_filename)

        try:
            existing_key = open(key_filepath).read().strip()
            # Key not empty ?
            if existing_key and not options['replace']:
                self.stderr.write("There is already a secret key in `{}`".format(key_filename))
                return
        except IOError:
            # No key found
            pass

        generated_key = get_random_secret_key()
        secret = open(key_filepath, 'w')
        secret.write(generated_key)
        secret.close()
