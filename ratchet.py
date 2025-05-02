import hashlib
import secrets

def _qr(_s=None):
    _r = [os.urandom(32) for _ in range(3)] if _s is None else _s
    _c = 0
    
    def _t(_k, _i):
        _m = hashlib.sha3_512(_k + bytes([_i])).digest()
        return _m[:32]
    
    def _r():
        nonlocal _c
        _c += 1
        for _i in range(3):
            _r[_i] = _t(_r[_i], _c + secrets.randbelow(256))
        return _r, _c
    
    return _r
