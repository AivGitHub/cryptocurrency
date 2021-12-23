import hashlib

import base58
import binascii
from django.db import models
import ecdsa
from mptt.models import MPTTModel, TreeForeignKey

from cryptocurrency.utils import get_BIP32Key_from_seed
from cryptocurrency.utils import get_eth_account


class Coin(models.Model):
    name = models.CharField(max_length=256)
    symbol = models.CharField(max_length=8, unique=True)

    class Meta:
        abstract = False

    def __str__(self) -> str:
        return self.name


class Wallet(MPTTModel):
    address = models.CharField(max_length=64, null=True, unique=True)
    public_key_hex = models.CharField(max_length=256)
    time_created = models.DateTimeField(auto_now_add=True)
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self) -> str:
        return self.address

    def get_address_from_private_key(self) -> str:
        ecdsa_private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        ecdsa_public_key = '04' + ecdsa_private_key.get_verifying_key().to_string().hex()

        hash256_from_ecdsa_public_key = hashlib.sha256(binascii.unhexlify(ecdsa_public_key)).hexdigest()
        ridemp160_from_hash256 = hashlib.new('ripemd160', binascii.unhexlify(hash256_from_ecdsa_public_key))

        prepend_network_byte = '00' + ridemp160_from_hash256.hexdigest()
        _hash = prepend_network_byte

        for x in range(1, 3):
            # double SHA256
            _hash = hashlib.sha256(binascii.unhexlify(_hash)).hexdigest()

        cheksum = _hash[:8]
        appended_checksum = prepend_network_byte + cheksum

        return base58.b58encode(binascii.unhexlify(appended_checksum)).decode('utf-8')

    @staticmethod
    def get_from_seed(seed: bytes = None, parent_seed: bytes = None, symbol: str = 'BTC') -> dict:
        if symbol == 'BTC':
            btc = get_BIP32Key_from_seed(seed=seed, parent_seed=parent_seed)

            return {
                'address': btc.Address(),
                'public_key_hex': btc.PublicKey().hex(),
                'private_key_hex': btc.PrivateKey().hex()
            }
        elif symbol == 'ETH':
            eth = get_eth_account(seed=seed, parent_seed=parent_seed)
            return {
                'address': eth.address,
                'public_key_hex': eth.key.hex(),
                'private_key_hex': eth.privateKey.hex()
            }
        else:
            raise NotImplementedError
