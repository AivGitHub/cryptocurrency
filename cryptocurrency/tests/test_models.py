from django.test import TestCase

from cryptocurrency.models import Wallet
from eth_account import Account


class WalletTestClass(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_from_seed(self):
        wrong_seed = 'a'
        wrong_parent_seed = 'b'
        wrong_symbol = 'wrong_symbol'
        btc_symbol = 'BTC'
        eth_symbol = 'ETH'
        seed = 'test is not that is alias as you know water not is get pole snow'

        with self.assertRaises(NotImplementedError):
            Wallet.get_from_seed(seed=seed.encode('utf-8'),
                                 parent_seed=seed.encode('utf-8'),
                                 symbol=wrong_symbol)

        with self.assertRaises(NotImplementedError):
            Wallet.get_from_seed(parent_seed=seed.encode('utf-8'),
                                 symbol=eth_symbol)

        with self.assertRaises(ValueError):
            Wallet.get_from_seed(seed=wrong_seed.encode('utf-8'),
                                 parent_seed=wrong_parent_seed.encode('utf-8'),
                                 symbol=btc_symbol)

        btc = Wallet.get_from_seed(seed=seed.encode('utf-8'), symbol=btc_symbol)
        eth = Wallet.get_from_seed(seed=seed.encode('utf-8'), symbol=eth_symbol)
        new_eth = Account.privateKeyToAccount(eth.get('private_key_hex'))

        self.assertEqual(btc.get('address'), '16Pm88xJ6cjmNZAPWkUAuqarSZ1Veshp7C')
        self.assertEqual(eth.get('address'), new_eth.address)
