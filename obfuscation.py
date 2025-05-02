import base64
import secrets
import numpy as np

def _qo():
    def _o(_d):
        _x = np.array(list(_d), dtype=np.uint8)
        _y = np.roll(_x, secrets.randbelow(256))
        _z = bytes(_y % 255)
        return base64.b64encode(_z + os.urandom(secrets.randbelow(16)))
    
    def _u(_d):
        _t = base64.b64decode(_d)[:-secrets.randbelow(16) or 1]
        _x = np.array(list(_t), dtype=np.uint8)
        _y = np.roll(_x, -secrets.randbelow(256))
        return bytes(_y % 255)
    
    return _o, _u
