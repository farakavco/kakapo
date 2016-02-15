# -*- coding: utf-8 -*-
from threading import local, get_ident
__author__ = 'vahid'

_thread_local = local()


class Context(dict):

    def __init__(self, thread_local, *args, **kw):
        super(Context, self).__init__(*args, **kw)
        self.thread_local = thread_local
        self.update({'__id': get_ident()})

    @classmethod
    def current(cls):
        if not hasattr(_thread_local, 'kakapo_context'):
            _thread_local.kakapo_context = cls(_thread_local)
        return _thread_local.kakapo_context

    def destroy(self):
        delattr(self.thread_local, 'kakapo_context')


class SingletonPerContext(type):

    def __call__(cls, *args, **kwargs):
        context_key = '%s' % cls.__name__
        context = Context.current()
        if context_key not in context:
            context[context_key] = super(SingletonPerContext, cls).__call__(*args, **kwargs)
        return context[context_key]
