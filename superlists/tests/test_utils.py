from django.test import TestCase
from superlists import settings as superlists_settings


class UtilsTest(TestCase):
    """Test any util functions"""

    def test_strtobool(self):
        for s in ['TRUE', 'True', 'true', 'TrUe', '1', 't', 'T']:
            self.assertTrue(superlists_settings.strtobool(s))
        # anything else should return false
        for s in ['False', '0', 'bla']:
            self.assertFalse(superlists_settings.strtobool(s))
