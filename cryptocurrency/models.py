import hashlib
import os

import base58
import binascii
import bip32utils
import ecdsa
from django.db import models
from mnemonic import Mnemonic


class Coin(models.Model):
    name = models.CharField(max_length=256)
    symbol = models.CharField(max_length=8)

    class Meta:
        abstract = False

    def __str__(self) -> str:
        return self.name


class Wallet(models.Model):
    address = models.CharField(max_length=36, null=True)
    public_key_hex = models.CharField(max_length=256)
    time_created = models.DateTimeField(auto_now_add=True)
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)

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
    def get_address_from_seed(seed=None) -> bip32utils:
        mnemonic = Mnemonic('english')

        if not seed:
            seed = mnemonic.to_seed(base58.b58encode(os.urandom(90)))

        # root_key = bip32utils.BIP32Key.fromEntropy(seed)
        # root_address = root_key.Address()
        # root_private_key = root_key.PrivateKey().hex()
        # root_public_hex = root_key.PublicKey().hex()
        # root_private_wif = root_key.WalletImportFormat()

        return bip32utils.BIP32Key.fromEntropy(seed)
