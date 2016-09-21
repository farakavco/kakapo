# -*- coding: utf-8 -*-
from threading import local, get_ident
__author__ = 'vahid'

_thread_local = local()


class Context(object):
    def __init__(self, *args, **kwargs):
        global _thread_local
        if hasattr(_thread_local, 'store'):
            raise AlreadyInitializedError('Context is already initialized')
        _thread_local.store = dict(*args, **kwargs)

    @classmethod
    def current(cls):
        return cls()

    @staticmethod
    def destroy():
        global _thread_local
        if hasattr(_thread_local, 'store'):
            delattr(_thread_local, 'store')

    def update(self, *args, **kwargs):
        global _thread_local
        if not hasattr(_thread_local, 'store'):
            raise ValueError('store not created yet')
        _thread_local.store.update(*args, **kwargs)

    @staticmethod
    def get(*args, **kwargs):
        global _thread_local
        return _thread_local.store.get(*args, **kwargs)

    @staticmethod
    def set(*args, **kwargs):
        global _thread_local
        _thread_local.store.set(*args, **kwargs)

    def __getitem__(self, key):
        global _thread_local
        return _thread_local.store[key]

    def __setitem__(self, key, value):
        global _thread_local
        _thread_local.store[key] = value

    def __delitem__(self, key):
        global _thread_local
        del _thread_local.store[key]

    def keys(self):
        global _thread_local
        return _thread_local.store.keys()


class SingletonPerContext(type):

    def __call__(cls, *args, **kwargs):
        context_key = '%s' % cls.__name__
        context = Context.current()
        if context_key not in context.keys():
            context[context_key] = super(SingletonPerContext, cls).__call__(*args, **kwargs)
        return context[context_key]


class AlreadyInitializedError(Exception):
    pass
