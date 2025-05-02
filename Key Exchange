import os
import secrets
import hashlib
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class _QSim:
    def __init__(self, _s=32):
        self._k = os.urandom(_s * 2)
    def _p(self):
        return self._k[:32]
    def _e(self, _pk):
        return os.urandom(32), os.urandom(32)
    def _d(self, _c):
        return os.urandom(32)

def _xk(_z=None, _a=None):
    _x = x25519.X25519PrivateKey.generate() if _z is None else _z
    _q = _QSim()
    _r = {'_x': _x, '_q': _q, '_a': _a, '_k': None}
    
    def _m(_b, _i):
        _s = _r['_k'] or _b
        _t = PBKDF2HMAC(
            algorithm=hashes.SHA3_512(),
            length=64,
            salt=hashlib.sha3_512(_s).digest(),
            iterations=100000 + (_i % 999)
        ).derive(_s)
        _u = HKDF(
            algorithm=hashes.SHA3_512(),
            length=96,
            salt=_t[:32],
            info=b'qs-xk-' + bytes([_i % 255])
        ).derive(_t)
        return [_u[:32], _u[32:64], _u[64:]]
    
    def _e():
        _p = _r['_x'].public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        if _r['_a']:
            _s1 = _r['_x'].exchange(x25519.X25519PublicKey.from_public_bytes(_r['_a']))
            _s2, _ = _r['_q']._e(_r['_a'][:32])
            _r['_k'] = hashlib.sha3_512(_s1 + _s2 + os.urandom(16)).digest()
        return _p, _m
    
    return _e

def _xp(_k):
    return x25519.X25519PublicKey.from_public_bytes(_k)
