from django.test import SimpleTestCase, override_settings
from django.conf import settings


class ProdSecuritySettingsTest(SimpleTestCase):
    @override_settings(DEBUG=False)
    def test_secure_settings_enabled(self):
        self.assertTrue(settings.SECURE_SSL_REDIRECT)
        self.assertTrue(settings.SESSION_COOKIE_SECURE)
        self.assertTrue(settings.CSRF_COOKIE_SECURE)
        self.assertEqual(settings.SECURE_HSTS_SECONDS, 63072000)
        self.assertTrue(settings.SECURE_HSTS_INCLUDE_SUBDOMAINS)
        self.assertTrue(settings.SECURE_HSTS_PRELOAD)
        self.assertEqual(settings.SECURE_REFERRER_POLICY, "same-origin")
