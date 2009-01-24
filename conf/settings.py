from django.conf import settings

NORMALISE_TO_UPPER = getattr(settings, 'ADB_NORMALISE_TO_UPPER', True)