# -*- coding: utf-8 -*-
import jwt
from kakapo.http.context import Context
__author__ = 'vahid'


class JwtBasePrincipal(object):
    def __init__(self, **kw):
        object.__setattr__(self, 'items', kw)

    @classmethod
    def _secret(cls):
        raise NotImplementedError

    @classmethod
    def _algorithm(cls):
        raise NotImplementedError

    def dump(self):
        res = jwt.encode(
            self.items,
            self._secret(),
            algorithm=self._algorithm())
        return res

    @classmethod
    def load(cls, s):
        params = jwt.decode(
            s,
            cls._secret(),
            algorithms=cls._algorithm())
        result = cls(**params)
        result.validate()
        return result

    def __getattr__(self, key):
        items = object.__getattribute__(self, 'items')
        if key in items:
            return items[key]
        raise AttributeError(key)

    def __setattr__(self, key, value):
        self.items[key] = value

    def __delattr__(self, key):
        del self.items[key]

    @classmethod
    def current(cls):
        current = Context.current()
        if current:
            return current.get('principal')
        return None

    @classmethod
    def get_current_member_id(cls):
        c = cls.current()
        if c:
            return c.id
        raise ValueError('Invalid principal')

    def validate(self):
        """
        It should be called just after the load method.
        You can include additional criteria to validate the principal.
        :return:
        """
        pass

    def put_into_context(self):
        ctx = Context.current()
        ctx['principal'] = self

    @staticmethod
    def delete_from_context():
        ctx = Context.current()
        ctx.pop('principal')
