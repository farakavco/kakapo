# -*- coding: utf-8 -*-
from wheezy.web.handlers import BaseHandler
from kakapo.http.context import Context
from kakapo.http.principal import JwtBasePrincipal
import jwt
__author__ = 'vahid'


class JwtPrincipalController(BaseHandler):
    __principal_type__ = JwtBasePrincipal
    __jwt_header_key__ = 'HTTP_X_JWT_TOKEN'

    def get_principal(self):
        ctx = Context.current()
        # if hasattr(self, '_JwtPrincipalController__principal'):
        #     return self.__principal

        if 'principal' in ctx.keys():
            return ctx['principal']

        if self.__jwt_header_key__ in self.request.environ:
            try:
                token_base64 = self.request.environ[self.__jwt_header_key__]
                ctx['principal'] = self.__principal_type__.load(token_base64)
                return ctx['principal']
            except jwt.exceptions.DecodeError:
                pass

        token = self.request.cookies.get('token')
        if token:
            ctx['principal'] = self.__principal_type__.load(token)
            return ctx['principal']

        return None

    def set_principal(self, principal):
        ctx = Context.current()
        ctx['principal'] = principal

    def del_principal(self):
        ctx['principal'] = None

    principal = property(get_principal, set_principal, del_principal)

    def has_route_args(self, *args):
        for name in args:
            if name not in self.route_args or self.route_args[name] is None:
                return False
        return True
