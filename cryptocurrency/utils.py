import os

import base58
import bip32utils
from mnemonic import Mnemonic


def get_BIP32Key_from_seed(seed: bytes = None, parent_seed: bytes = None) -> bip32utils:
    mnemonic = Mnemonic('english')

    if parent_seed:
        root_key = bip32utils.BIP32Key.fromEntropy(parent_seed)
        return root_key.ChildKey(0).ChildKey(0)

    if not seed:
        seed = mnemonic.to_seed(base58.b58encode(os.urandom(90)))

    return bip32utils.BIP32Key.fromEntropy(seed)
