# -*- coding: utf-8 -*-
import threading
__author__ = 'vahid'

local = threading.local()


class Context(object):
    def __init__(self, *args, **kwargs):

        if not hasattr(local, 'store'):
            local.store = []

        local.store.append(dict(*args, **kwargs))

    @classmethod
    def current(cls):
        return cls()

    @staticmethod
    def destroy():
        if hasattr(local, 'store'):
            local.store.pop()

    def update(self, *args, **kwargs):
        if not hasattr(local, 'store'):
            raise ValueError('store not created yet')
        local.store.update(*args, **kwargs)

    @staticmethod
    def get(*args, **kwargs):
        return local.store.get(*args, **kwargs)

    @staticmethod
    def set(*args, **kwargs):
        local.store.set(*args, **kwargs)

    def __getitem__(self, key):
        return local.store[key]

    def __setitem__(self, key, value):
        local.store[key] = value

    def __delitem__(self, key):
        del local.store[key]

    def keys(self):
        return local.store.keys()


class SingletonPerContext(type):

    def __call__(cls, *args, **kwargs):
        context_key = '%s' % cls.__name__
        context = Context.current()
        if context_key not in context.keys():
            context[context_key] = \
                super(SingletonPerContext, cls).__call__(*args, **kwargs)
        return context[context_key]


class AlreadyInitializedError(Exception):
    pass
