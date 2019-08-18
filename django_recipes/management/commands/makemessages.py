from django.core.management.commands import makemessages


class Command(makemessages.Command):
    def add_arguments(self, parser):
        parser.add_argument('--use-fuzzy-matching', action='store_true', default=False)

        super().add_arguments(parser)

    def handle(self, *args, **options):
        if not options['use_fuzzy_matching']:
            self.msgmerge_options.remove('--no-fuzzy-matching')  # Do not use fuzzy matching!

        return super().handle(*args, **options)
