# Copyright (c) 2019, CZ.NIC, z.s.p.o. (http://www.nic.cz/)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the CZ.NIC nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL CZ.NIC BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
from uci import Uci, UciException, UciExceptionNotFound


class EUci(Uci):
    """Extended Uci wrapper
    """
    __BOOLEAN_VALUES = {
        "0": False,
        "no": False,
        "off": False,
        "false": False,
        "disabled": False,
        "1": True,
        "yes": True,
        "on": True,
        "true": True,
        "enabled": True,
    }
    __BOOLEAN_TRUE = "1"
    __BOOLEAN_FALSE = "0"

    def get(self, *args, dtype=str, **kwargs):
        """Get configuration value.

        Up to three positional arguments are expected. Those are uci "config"
        "section" and "option" in this order.

        Following additional optional keywords arguments are available:
        dtype: data type to be returned. Currently supported are: str, bool and
            int. If you don't specify this then it defaults to str. If value
            cannot be converted to specified type then it raises ValueError.
        default: default value to be returned instead of raising
            UciExceptionNotFound.

        When requested value is not found then this raises UciExceptionNotFound.
        """
        kwdiff = set(kwargs).difference({'default'})
        if kwdiff:
            raise TypeError("'{}' is an invalid keyword argument for this function".format(kwdiff))

        try:
            value = super().get(*args)
        except UciExceptionNotFound:
            if 'default' not in kwargs:
                raise
            value = str(kwargs['default'])

        if dtype == str:
            return value
        if dtype == bool:
            value = value.lower()
            if value not in self.__BOOLEAN_VALUES:
                raise ValueError
            return self.__BOOLEAN_VALUES[value]
        if dtype == int:
            return int(value)
        raise TypeError("'{}' is not supported type of data".format(dtype))

    def set(self, *args, **kwargs):
        """Set configuration value.

        Up to three positional arguments specifying configuration can be
        specified. Those are "config", "section" and "option". Option does not
        have to be specified and in such case section value is set. Last
        positional argument (third or fourth one) is value to be set. This
        function automatically detect that argument type and sets value
        according to that. Supported types are: str, bool and int.
        If provided value is not of any of these types then it is converted to
        string.

        It is suggested to always explicitly type last positional argument to
        ensure correct type. That is in case of boolean for example:
        set("foo", "fee", "faa", bool(value))
        """
        kwdiff = set(kwargs).difference({})
        if kwdiff:
            raise TypeError("'{}' is an invalid keyword argument for this function".format(kwdiff))

        dtype = type(args[-1])
        if dtype == bool:
            value = self.__BOOLEAN_TRUE if args[-1] else self.__BOOLEAN_FALSE
        else:
            # This implements handler for str and int type as well as fallback
            value = str(args[-1])
        super().set(*args[:-1], value)

    def get_boolean(self, *args, **kwargs):
        """This is obsolete! Please use instead: set(config, section, option, dtype=bool)
        Returns given UCI config as a boolean.
        Value '0', 'no', 'off', 'false' or 'disabled' is returned as False.
        Value '1' , 'yes', 'on', 'true' or 'enabled' is returned as True.
        ValueError is raised on any other value.
        """
        return self.get(*args, dtype=bool, **kwargs)

    def set_boolean(self, *args):
        """This is obsolete! Please use instead: set(config, section, option, value, bool(value))
        Sets boolean value to given UCI config.
        """
        self.set(*args[:-1], bool(args[-1]))

    def get_integer(self, *args, **kwargs):
        """This is obsolete! Please use instead: set(config, section, option, dtype=int)
        Returns given UCI config as an integer.
        Raises ValueError if config value can't be converted to int.
        """
        return self.get(*args, dtype=int, **kwargs)

    def set_integer(self, *args):
        """This is obsolete! Please use instead: set(config, section, option, value, int(value))
        Sets integer to given UCI config.
        """
        self.set(*args[:-1], int(args[-1]))
