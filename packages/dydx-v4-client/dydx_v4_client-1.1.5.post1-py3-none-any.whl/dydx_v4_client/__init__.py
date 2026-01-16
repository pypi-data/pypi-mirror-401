from enum import IntEnum
from ._bootstrap import init

class OrderFlags(IntEnum):
    SHORT_TERM = 0
    LONG_TERM = 64
    CONDITIONAL = 32
    
init()

MAX_CLIENT_ID = 2**32 - 1
