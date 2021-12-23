from django.test import TestCase

from cryptocurrency.models import Wallet


class WalletTestClass(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_from_seed(self):
        wrong_seed = 'a'
        wrong_parent_seed = 'b'
        wrong_symbol = 'wrong_symbol'
        symbol = 'BTC'
        seed = 'test is not that is alias as you know water not is get pole snow'

        with self.assertRaises(NotImplementedError):
            Wallet.get_from_seed(seed=seed.encode('utf-8'),
                                 parent_seed=seed.encode('utf-8'),
                                 symbol=wrong_symbol)

        with self.assertRaises(ValueError):
            Wallet.get_from_seed(seed=wrong_seed.encode('utf-8'),
                                 parent_seed=wrong_parent_seed.encode('utf-8'),
                                 symbol=symbol)

        BIP32Key = Wallet.get_from_seed(seed=seed.encode('utf-8'), symbol='BTC')

        self.assertEqual(BIP32Key.Address(), '16Pm88xJ6cjmNZAPWkUAuqarSZ1Veshp7C')
