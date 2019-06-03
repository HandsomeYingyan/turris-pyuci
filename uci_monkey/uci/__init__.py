"""Unified configuration interface bindings
"""


class Uci():
    """Top level entry point to uci context. Create instance of this for any
    uci access
    """

    def __init__(self, savedir=None, confdir=None):
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass


class UciException(Exception):
    pass


class UciExceptionNotFound(UciException):
    pass
