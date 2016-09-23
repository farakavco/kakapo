# -*- coding: utf-8 -*-
import threading
__author__ = 'vahid'

local = threading.local()


class Context(object):
    def __init__(self, proxy_only=False, *args, **kwargs):
        if proxy_only:
            return

        if not hasattr(local, 'store'):
            local.store = []

        local.store.append(dict(*args, **kwargs))

    @classmethod
    def current(cls):
        return cls(proxy_only=True)

    @staticmethod
    def destroy():
        if hasattr(local, 'store'):
            del local.store[-1]

    def __getitem__(self, key):
        return local.store[-1][key]

    def __setitem__(self, key, value):
        local.store[-1][key] = value

    def __delitem__(self, key):
        del local.store[-1][key]

    def __getattr__(self, name):
        if not hasattr(local, 'store'):
            raise ContextNotInitializedError
        return getattr(local.store[-1], name)


class SingletonPerContext(type):

    def __call__(cls, *args, **kwargs):
        context_key = '%s' % cls.__name__
        context = Context.current()
        if context_key not in context.keys():
            context[context_key] = \
                super(SingletonPerContext, cls).__call__(*args, **kwargs)
        return context[context_key]


class ContextNotInitializedError(Exception):
    pass
