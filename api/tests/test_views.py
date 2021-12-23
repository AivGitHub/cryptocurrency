from django.test import TestCase

from api.views import WalletViews
from django.http import HttpRequest


class TestWalletViews(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get(self):
        request = HttpRequest()
        views = WalletViews()

        self.assertEqual(views.get(request).status_code, 200)

