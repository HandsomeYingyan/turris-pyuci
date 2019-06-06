"""Unified configuration interface bindings
"""
import collections
import threading

_state = None
_state_lock = threading.Lock()


class Uci():
    """Top level entry point to uci context. Create instance of this for any
    uci access
    """

    def __init__(self, savedir=None, confdir=None):
        self.tainted = False

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.tainted:
            for config in self.list_configs():
                self.commit(config)

    def _option(self, value):
        if isinstance(value, collections.Iterable) and not isinstance(value, str):
            return tuple(str(el) for el in value)
        return str(value)

    def _section(self, section):
        result = {}
        for name, value in section.items():
            result[str(name)] = self._option(value)
        return result

    def _package(self, package):
        result = {}
        for name, value in package.items():
            result[name] = self._section(value)
        return result

    def _lookup(self, *args):
        handler = {
            1: lambda: _state[args[0]],
            2: lambda: _state[args[0]][args[1]],
            3: lambda: _state[args[0]][args[1]][args[2]],
        }
        if len(args) not in handler:
            # TODO match exception with Uci one
            raise Exception("Invalid number of arguments")
        # TODO check if every level has appropriate field
        return handler[len]()

    def _get(self, all, *args):
        itm = self._lookup(args)
        if len(args) == 2 and not all:
            return str(itm.type())
        handler = {
            1: self._package,
            2: self._section,
            3: self._option
        }
        return handler[len(args)](*args)

    def get(self, *args):
        return self._get(False, *args)

    def get_all(self, *args):
        return self._get(True, *args)

    def set(self, *args):
        self.tainted = True
        raise NotImplementedError

    def delete(self, *args):
        self.tainted = True
        raise NotImplementedError

    def add(self, *args):
        self.tainted = True
        raise NotImplementedError

    def rename(self, *args):
        self.tainted = True
        raise NotImplementedError

    def reorder(self, *args):
        self.tainted = True
        raise NotImplementedError

    def save(self, *args):
        raise NotImplementedError

    def commit(self, *args):
        raise NotImplementedError
        self.tainted = False

    def revert(self, *args):
        raise NotImplementedError
        self.tainted = False

    def unload(self, *args):
        raise NotImplementedError

    def load(self, *args):
        raise NotImplementedError

    def changes(self, *args):
        raise NotImplementedError

    def list_configs(self):
        raise NotImplementedError

    def confdir(self):
        raise NotImplementedError

    def set_confdir(self, path):
        raise NotImplementedError

    def savedir(self):
        raise NotImplementedError

    def set_savedir(self, path):
        raise NotImplementedError


class UciException(Exception):
    pass


class UciExceptionNotFound(UciException):
    pass
