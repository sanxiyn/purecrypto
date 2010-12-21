from ctypes import *
from ctypes.util import find_library

nss = CDLL(find_library('nss3'))
nss.NSS_NoDB_Init(None)

nss.HASH_Clone
nss.HASH_Create
nss.HASH_Destroy
nss.HASH_End
nss.HASH_ResultLenContext
nss.HASH_Update

_hash_mapping = {
    'MD2': 1,
    'MD5': 2,
    'SHA1': 3,
    'SHA256': 4,
    'SHA384': 5,
    'SHA512': 6,
}

class Hash:

    @staticmethod
    def new(name):
        name = name.upper()
        if name not in _hash_mapping:
            raise ValueError('unsupported hash type')
        context = nss.HASH_Create(_hash_mapping[name])
        return Hash(context)

    def __init__(self, context):
        self.context = context
        self.digest_size = nss.HASH_ResultLenContext(context)

    def __del__(self):
        nss.HASH_Destroy(self.context)

    def update(self, string):
        nss.HASH_Update(self.context, string, len(string))

    def _copy_context(self):
        context = nss.HASH_Clone(self.context)
        return context

    def copy(self):
        context = self._copy_context()
        return Hash(context)

    def digest(self):
        context = self._copy_context()
        buffer = create_string_buffer(self.digest_size)
        size = c_int()
        nss.HASH_End(context, buffer, byref(size), self.digest_size)
        return buffer.raw[:size.value]

    def hexdigest(self):
        return self.digest().encode('hex')
