import os
import hmac
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
from cryptography.exceptions import InvalidKey

def _qe(_k, _r, _s):
    def _c(_p, _m=b'', _n=None):
        _n = _n or os.urandom(12)
        _a = AESGCM(_k[0])
        _t1 = _a.encrypt(_n, _p, _m)
        
        _b = Cipher(algorithms.Salsa20(_k[1], _n[:8]), mode=None).encryptor()
        _t2 = _b.update(_t1) + _b.finalize()
        
        _c = ChaCha20Poly1305(_k[2])
        _t3 = _c.encrypt(_n, _t2, _m)
        
        _h = hmac.new(_s[0], _m + _t3 + _n, hashlib.sha3_512).digest()
        _p = os.urandom(_r % 64)
        return _n + _t3 + _h + _p
    
    def _d(_ct, _m=b''):
        if len(_ct) < 76:
            raise ValueError("Invalid ciphertext")
        
        _n, _ct, _h = _ct[:12], _ct[:-64], _ct[-64:-(_r % 64) or 1]
        _v = hmac.new(_s[0], _m + _ct + _n, hashlib.sha3_512).digest()
        if not hmac.compare_digest(_v, _h):
            raise ValueError("HMAC failure")
        
        _c = ChaCha20Poly1305(_k[2])
        try:
            _t2 = _c.decrypt(_n, _ct, _m)
        except InvalidKey:
            raise ValueError("Decryption failure")
        
        _b = Cipher(algorithms.Salsa20(_k[1], _n[:8]), mode=None).decryptor()
        _t1 = _b.update(_t2) + _b.finalize()
        
        _a = AESGCM(_k[0])
        _p = _a.decrypt(_n, _t1, _m)
        return _p
    
    return _c, _d
