# -*- coding: utf-8 -*-
from wheezy.web.handlers import BaseHandler
from kakapo.http.context import Context
from kakapo.http.principal import JwtBasePrincipal
import jwt


class JwtPrincipalController(BaseHandler):
    __principal_type__ = JwtBasePrincipal
    __jwt_header_key__ = 'HTTP_X_JWT_TOKEN'

    def get_principal(self):
        ctx = Context.current()
        if 'principal' in ctx.keys():
            return ctx['principal']
        return None

    def set_principal(self, principal):
        ctx = Context.current()
        ctx['principal'] = principal

    def del_principal(self):
        ctx = Context.current()
        ctx['principal'] = None

    principal = property(get_principal, set_principal, del_principal)

    def has_route_args(self, *args):
        for name in args:
            if name not in self.route_args or self.route_args[name] is None:
                return False
        return True

    def load_principal(self, from_cookie=True):
        send_to_client = False

        token = self.request.environ.get(self.__jwt_header_key__)
        if not token and from_cookie:
            token = self.request.cookies.get('token')

        if token is None:
            return None, send_to_client

        try:
            return self.__principal_type__.load(token), send_to_client
        except Exception:
            return None, send_to_client
