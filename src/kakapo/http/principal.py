# -*- coding: utf-8 -*-
from jose import jwt
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
        token = jwt.encode(
            self.items,
            self._secret(),
            algorithm=self._algorithm())
        return token

    @classmethod
    def load(cls, s):
        params = jwt.decode(
            s,
            cls._secret(),
            algorithms=cls._algorithm())
        principal = cls(**params)
        principal.validate()
        return principal

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
        return current.get('principal')

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
        del ctx['principal']

    @classmethod
    def from_user(cls, user):
        raise NotImplementedError

    @classmethod
    def login(cls, user):
        principal = cls.from_user(user)
        principal.put_into_context()

    @classmethod
    def logout(cls):
        cls.delete_from_context()
