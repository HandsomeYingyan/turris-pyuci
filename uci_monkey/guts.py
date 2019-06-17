"""These are abstraction for building and managing uci_monkey internal
configuration representation.
"""
import re
import collections
import threading
from copy import copy
from . import uci


class UciDir(dict):
    """UCI configuration state. It allows you to overly and in general
    manage current UCI configuration. Just instanciate it to create new state
    overlay. To drop it you call drop().
    Note that states automatically create linked-list chain.
    """

    def __init__(self, *args, **kwargs):
        self.lock = threading.Lock()
        self._re_option = re.compile(r'\w+')
        self._re_section = re.compile(r'\w+|@\w+\[\d+\]')
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        pkey = key.split('.')
        if not 2 <= len(pkey) <= 3:
            raise InvalidUciSpecException("Only allowed keys are of form: config.section[.option]")
        if not self._re_option.fullmatch(pkey[0]):
            raise InvalidUciSpecException("Section 'config' does not conform to appropriate format")
        if not self._re_section.fullmatch(pkey[1]):
            raise InvalidUciSpecException("Section 'section' does not conform to appropriate format")
        if len(pkey) == 3 and not self._re_option.fullmatch(pkey[2]):
            raise InvalidUciSpecException("Section 'option' does not conform to appropriate format")
        if len(pkey) == 3 and isinstance(value, collections.Iterable) and not isinstance(value, str):
            super().__setitem__(key, list(value))
        else:
            super().__setitem__(key, str(value))


class UciState(dict):
    """UCI configuration state. It allows you to overly and in general
    manage current UCI configuration. Just instanciate it to create new state
    overlay. To drop it you call drop().
    Note that states automatically create linked-list chain.
    """

    def __setitem__(self, path, value):
        if not isinstance(value, UciDir):
            raise TypeError("'{}' is not of UciDir instance".format(type(value)))
        super().__setitem__(path, list(value))

    def __missing__(self, key):
        self[key] = UciDir()
        return self[key]

    def conf(self):
        """Returns default directory for confdir."""
        return self["/etc/config"]

    def save(self):
        """Returns default directory for savedir."""
        return self["/tmp/.uci"]


class InvalidUciSpecException(Exception):
    """Provided UCI config.section.option specifier is invalid.
    """
