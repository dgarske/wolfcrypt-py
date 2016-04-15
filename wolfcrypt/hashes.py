# hashes.py
#
# Copyright (C) 2006-2016 wolfSSL Inc.
#
# This file is part of wolfSSL. (formerly known as CyaSSL)
#
# wolfSSL is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# wolfSSL is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
from wolfcrypt._hashes import ffi
from wolfcrypt._hashes import lib


class _Hash(object):
    # Magic object that protects against constructors.
    _JAPANESE_CYBER_SWORD = object()


    def __init__(self, token=""):
        if token is not self._JAPANESE_CYBER_SWORD:
            # PEP 247 -- API for Cryptographic Hash Functions
            raise ValueError("don't construct directly, use new([string])")


    def copy(self):
        copy = self.new()

        ffi.memmove(copy._native_object,
                    self._native_object,
                    self._native_size)

        return copy


    def update(self, string):
        self._update(string)


    def digest(self):
        ret = "\0" * self.digest_size

        if self._native_object:
            obj = ffi.new(self._native_type)

            ffi.memmove(obj, self._native_object, self._native_size)

            self._final(obj, ret)

        return ret


    def hexdigest(self):
        return "".join("{:02x}".format(ord(c)) for c in self.digest())


class _UnkeyedHash(_Hash):
    @classmethod
    def new(cls, string=None):
        self = cls(cls._JAPANESE_CYBER_SWORD)

        self._native_object = ffi.new(self._native_type)

        self._init()

        if (string):
            self._update(string)

        return self


# Hmac types

_TYPE_SHA    = 1
_TYPE_SHA256 = 2
_TYPE_SHA384 = 5
_TYPE_SHA512 = 4
_HMAC_TYPES = [_TYPE_SHA, _TYPE_SHA256, _TYPE_SHA384, _TYPE_SHA512]


class _Hmac(_Hash):
    digest_size  = None
    _native_type = "Hmac *"
    _native_size = ffi.sizeof("Hmac")

    @classmethod
    def new(cls, type, key, string=None):
        self = cls(cls._JAPANESE_CYBER_SWORD)

        self._native_object = ffi.new(self._native_type)

        self._init(type, key)

        if (string):
            self._update(string)

        return self


    def _init(self, type, key):
        lib.wc_HmacSetKey(self._native_object, type, key, len(key))


    def _update(self, data):
        lib.wc_HmacUpdate(self._native_object, data, len(data))


    def _final(self, obj, ret):
        lib.wc_HmacFinal(obj, ret)


class Sha(_UnkeyedHash):
    digest_size  = 20
    _native_type = "Sha *"
    _native_size = ffi.sizeof("Sha")


    def _init(self):
        lib.wc_InitSha(self._native_object)


    def _update(self, data):
        lib.wc_ShaUpdate(self._native_object, data, len(data))


    def _final(self, obj, ret):
        lib.wc_ShaFinal(obj, ret)


class HmacSha(_Hmac):
    @classmethod
    def new(cls, key, string=None):
        self = _Hmac.new(_TYPE_SHA, key, string)
        self.digest_size = Sha.digest_size

        return self


class Sha256(_UnkeyedHash):
    digest_size  = 32
    _native_type = "Sha256 *"
    _native_size = ffi.sizeof("Sha256")


    def _init(self):
        lib.wc_InitSha256(self._native_object)


    def _update(self, data):
        lib.wc_Sha256Update(self._native_object, data, len(data))


    def _final(self, obj, ret):
        lib.wc_Sha256Final(obj, ret)


class HmacSha256(_Hmac):
    @classmethod
    def new(cls, key, string=None):
        self = _Hmac.new(_TYPE_SHA256, key, string)
        self.digest_size = Sha256.digest_size

        return self


class Sha384(_UnkeyedHash):
    digest_size  = 48
    _native_type = "Sha384 *"
    _native_size = ffi.sizeof("Sha384")


    def _init(self):
        lib.wc_InitSha384(self._native_object)


    def _update(self, data):
        lib.wc_Sha384Update(self._native_object, data, len(data))


    def _final(self, obj, ret):
        lib.wc_Sha384Final(obj, ret)


class HmacSha384(_Hmac):
    @classmethod
    def new(cls, key, string=None):
        self = _Hmac.new(_TYPE_SHA384, key, string)
        self.digest_size = Sha384.digest_size

        return self


class Sha512(_UnkeyedHash):
    digest_size  = 64
    _native_type = "Sha512 *"
    _native_size = ffi.sizeof("Sha512")


    def _init(self):
        lib.wc_InitSha512(self._native_object)


    def _update(self, data):
        lib.wc_Sha512Update(self._native_object, data, len(data))


    def _final(self, obj, ret):
        lib.wc_Sha512Final(obj, ret)


class HmacSha512(_Hmac):
    @classmethod
    def new(cls, key, string=None):
        self = _Hmac.new(_TYPE_SHA512, key, string)
        self.digest_size = Sha512.digest_size

        return self