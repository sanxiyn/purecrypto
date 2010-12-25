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

    @classmethod
    def new(cls, name):
        algorithm = libgcrypt.gcry_md_map_name(name)
        if not algorithm:
            raise ValueError('unsupported hash type')
        context = c_void_p()
        libgcrypt.gcry_md_open(byref(context), algorithm, 0)
        return cls(context)

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

libgcrypt.gcry_cipher_close
libgcrypt.gcry_cipher_decrypt
libgcrypt.gcry_cipher_encrypt
libgcrypt.gcry_cipher_map_name
libgcrypt.gcry_cipher_open
libgcrypt.gcry_cipher_setiv
libgcrypt.gcry_cipher_setkey

MODE_ECB = 1
MODE_CBC = 3
MODE_CFB = 2
MODE_OFB = 5
MODE_CTR = 6

class Cipher:

    def __init__(self, context):
        self.context = context

    def __del__(self):
        libgcrypt.gcry_cipher_close(self.context)

    def encrypt(self, string):
        size = len(string)
        buffer = create_string_buffer(size)
        libgcrypt.gcry_cipher_encrypt(self.context, buffer, size, string, size)
        return buffer.raw

    def decrypt(self, string):
        size = len(string)
        buffer = create_string_buffer(size)
        libgcrypt.gcry_cipher_encrypt(self.context, buffer, size, string, size)
        return buffer.raw

def make_new(name):
    algorithm = libgcrypt.gcry_cipher_map_name(name)
    def new(key, mode, iv):
        context = c_void_p()
        libgcrypt.gcry_cipher_open(byref(context), algorithm, mode, 0)
        libgcrypt.gcry_cipher_setkey(context, key, len(key))
        libgcrypt.gcry_cipher_setiv(context, iv, len(iv))
        return Cipher(context)
    return new
