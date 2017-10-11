# -*- coding: utf-8 -*-

import base64
from Crypto.Cipher import AES

# the block size for the cipher object; must be 16 per FIPS-197
_BLOCK_SIZE = 16

# the character used for padding--with a block cipher such as AES, the value
# you encrypt must be a multiple of BLOCK_SIZE in length.  This character is
# used to ensure that your value is always a multiple of BLOCK_SIZE
_PADDING = '{'

# one-liner to sufficiently pad the text to be encrypted
_pad = lambda s: s + (_BLOCK_SIZE - len(s) % _BLOCK_SIZE) * _PADDING

# one-liners to encrypt/encode and decrypt/decode a string
# encrypt with AES, encode with base64
_encodeAES = lambda c, s: base64.b64encode(c.encrypt(_pad(s))).decode('utf-8')

def _decodeAES(c, e):
    e = e.encode('utf-8')
    decoded = base64.b64decode(e)
    decrypted = c.decrypt(decoded).decode('utf-8')
    return decrypted.rstrip(_PADDING)

# a random secret key
_SECRET = b'{\x82\xcc\xde\x03L\x1142\x9a\x94\xd6\xb1\xc5\xd4\xc6'

if len(_SECRET) > _BLOCK_SIZE:
    _SECRET = _SECRET[:_BLOCK_SIZE] 

# create a cipher object using the random secret
_cipher = AES.new(_SECRET)


def aes_encode(password):
    # encode a string
    result = _encodeAES(_cipher, password)
    return result

def aes_decode(password):
    result = _decodeAES(_cipher, password)
    return result

# just export necessary methods
__all__ = ['aes_encode', 'aes_decode']