"""These are abstraction for building and managing uci_monkey internal
configuration representation.
"""
import string
import random
import collections
from . import uci

_ANONYM_CONF_LEN = 6
_anonym_conf_name_v = set()


def _anonym_conf_name():
    """Generates new name for anonymous sections.
    """
    global _anonymous_conf_name_v
    value = ''.join(random.choices(string.ascii_lowercase + string.digits, k=_ANONYM_CONF_LEN))
    if value in _anonym_conf_name_v:
        return _anonym_conf_name()
    _anonym_conf_name_v.add(value)
    return "cfg" + value


class UciState(dict):
    """Top level configuration state. It allows you to overly and in general
    manage current UCI configuration. Just instanciate it to create new state
    overlay. To drop it you call wipe().
    Note that states automatically create linked-list chain.
    """

    def __init__(self, extend, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extends = extend
        self.parent = uci._state
        uci._state = self

    def __del__(self):
        self.drop()

    def __setitem__(self, key, value):
        if not isinstance(value, UciConfig):
            raise TypeError("Only instances of UciConfig can be assigned")
        super().__setitem__(key, value)

    def __missing__(self, key):
        if self.extends:
            return self.parent[key]
        raise KeyError(key)

    def drop(self):
        """Drop this state from Uci. This causes also removal of all states
        instanciated created after this one (child states).
        """
        # TODO free all up to this state from current one
        uci._state = self.parent


class UciConfig(collections.OrderedDict):
    """Container for Uci sections. It replaces UCI configuration file.
    """

    def __init__(self, *args, **kwargs):
        rargs = list(args)
        for arg in rargs:
            if isinstance(arg, UciSection):  # This is anonymous section
                kwargs[_anonym_conf_name()] = arg
                rargs.remove(arg)
        super().__init__(*rargs, **kwargs)

    def __setitem__(self, key, value):
        if not isinstance(value, UciSection):
            raise TypeError("Only instances of UciConfig can be assigned")
        super().__setitem__(key, value)

    def add(self, section):
        """Add anonymous section.
        """
        self[_anonym_conf_name()] = section


class UciSection(dict):
    """Container for lists and options. Section can also have name (value).
    """

    def __init__(self, type, *args, **kwargs):
        self._type = type
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        if not isinstance(value, collections.Iterable):
            raise TypeError("Only strings and interables can be assigned")
        super().__setitem__(key, value)

    def type(self):
        """Return type of this section.
        """
        return self.type
