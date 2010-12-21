# PureCrypto

This is a [Python](http://www.python.org/) binding to cryptographic libraries
using [ctypes](http://docs.python.org/library/ctypes.html).
It can be used with [PyPy](http://pypy.org/), for example.

Currently, following libraries are supported:

* [Libgcrypt](http://www.gnupg.org/documentation/manuals/gcrypt/)

This module intends to follow
[PEP 247](http://www.python.org/dev/peps/pep-0247/) and
[PEP 272](http://www.python.org/dev/peps/pep-0272/)
in API for cryptographic hash functions and block encryption algorithms.

Related projects include:

* [PyCrypto](http://www.dlitz.net/software/pycrypto/),
which you probably should use if you can.
* [ctypescrypto](http://code.google.com/p/ctypescrypto/) and its fork
[jaraco.crypto](https://bitbucket.org/jaraco/jaraco.crypto),
a Python binding to [OpenSSL](http://www.openssl.org/) using ctypes.
* [Libgcrypt-py](http://libgcrypt-py.sourceforge.net/),
a Python binding to Libgcrypt using C extension.
