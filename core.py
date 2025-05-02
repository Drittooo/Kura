import secrets
from key_exchange import _xk, _xp
from ratchet import _qr
from encryption import _qe
from obfuscation import _qo

class VLESSQuantumShadow:
    def __init__(self, _x=secrets.token_bytes(16), _y=None):
        self._h = _xk(None, _y)
        self._r = _qr()
        self._o = _qo()
        self._c = None
        self._i = 0
    
    def _p(self):
        _pk, _km = self._h()
        self._c = _qe(_km(self._r()[0], self._i), self._i, self._r())
        return _pk
    
    def _s(self, _pk):
        self._h = _xk(_xp(_pk), _pk)
        self._p()
    
    def encrypt_packet(self, _pt, _m=b''):
        if not self._c:
            self._p()
        
        _e = self._c[0](_pt, _m)
        _o = self._o[0](_e)
        
        self._i += 1
        if self._i % (secrets.randbelow(8) + 1) == 0:
            self._r()
        
        return _o
    
    def decrypt_packet(self, _ct, _m=b''):
        if not self._c:
            self._p()
        
        _d = self._o[1](_ct)
        _p = self._c[1](_d, _m)
        return _p

if __name__ == "__main__":
    _s = VLESSQuantumShadow()
    _c = VLESSQuantumShadow()
    
    _sp = _s._p()
    _cp = _c._p()
    
    _s._s(_cp)
    _c._s(_sp)
    
    _m = b"metadata:xyz"
    _p = b"Secret VLESS data"
    
    _e = _c.encrypt_packet(_p, _m)
    _d = _s.decrypt_packet(_e, _m)
    
    print(f"Original: {_p}")
    print(f"Decrypted: {_d}")
