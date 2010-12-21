from ctypes import *
from ctypes.util import find_library

libgcrypt = CDLL(find_library('gcrypt'))

libgcrypt.gcry_md_close
libgcrypt.gcry_md_copy
libgcrypt.gcry_md_get_algo
libgcrypt.gcry_md_get_algo_dlen
libgcrypt.gcry_md_map_name
libgcrypt.gcry_md_open
libgcrypt.gcry_md_read
libgcrypt.gcry_md_write

class Hash:

    @staticmethod
    def new(name):
        algorithm = libgcrypt.gcry_md_map_name(name)
        if not algorithm:
            raise ValueError('unsupported hash type')
        context = c_void_p()
        libgcrypt.gcry_md_open(byref(context), algorithm, 0)
        return Hash(context)

    def __init__(self, context):
        self.context = context
        algorithm = libgcrypt.gcry_md_get_algo(context)
        self.digest_size = libgcrypt.gcry_md_get_algo_dlen(algorithm)

    def __del__(self):
        libgcrypt.gcry_md_close(self.context)

    def update(self, string):
        libgcrypt.gcry_md_write(self.context, string, len(string))

    def _copy_context(self):
        context = c_void_p()
        libgcrypt.gcry_md_copy(byref(context), self.context)
        return context

    def copy(self):
        context = self._copy_context()
        return Hash(context)

    def digest(self):
        context = self._copy_context()
        address = libgcrypt.gcry_md_read(context, 0)
        return string_at(address, self.digest_size)

    def hexdigest(self):
        return self.digest().encode('hex')
