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
        if not hasattr(local, 'store'):
            return cls()
        return cls(proxy_only=True)

    @staticmethod
    def destroy():
        if not hasattr(local, 'store'):
            return

        try:
            del local.store[-1]
        except IndexError:
            pass

        if not local.store:
            delattr(local, 'store')

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


application_context = {}


class SingletonPerApplication(type):
    def __call__(cls, *args, **kwargs):
        global application_context
        context_key = '%s' % cls.__name__
        if context_key not in application_context.keys():
            application_context[context_key] = \
                super(SingletonPerApplication, cls).__call__(*args, **kwargs)
        return application_context[context_key]


class ContextNotInitializedError(Exception):
    pass
