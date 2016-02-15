# -*- coding: utf-8 -*-
from wheezy.web.handlers import BaseHandler
from kakapo.http.context import Context
from kakapo.http.principal import JwtBasePrincipal
import jwt
__author__ = 'vahid'


class JwtPrincipalController(BaseHandler):
    __principal_type__ = JwtBasePrincipal
    __jwt_header_key__ = 'HTTP_X_JWT_TOKEN'

    @property
    def context(self):
        return Context.current()

    def get_principal(self):
        if hasattr(self, '_JwtPrincipalController__principal'):
            return self.__principal

        if self.__jwt_header_key__ in self.request.environ:
            try:
                token_base64 = self.request.environ[self.__jwt_header_key__]
                self.__principal = self.__principal_type__.load(token_base64)
                return self.__principal
            except jwt.exceptions.DecodeError:
                pass

        token = self.request.cookies.get('token')
        if token:
            self.__principal = self.__principal_type__.load(token)
            return self.__principal

        # # TODO: DELETE THESE LINES
        # if 'HTTP_X_BYPASS_AUTH' in self.request.environ:
        #     return self.__principal_type__(
        #         id=1,
        #         email='admin@falcon.com',
        #         roles=['admin'],
        #         role_ids=[1],
        #         alias='admin')

        return None

    def set_principal(self, principal):
        self.__principal = principal
        self.context.update({
            'principal': principal
        })

    def del_principal(self):
        self.__principal = None

    principal = property(get_principal, set_principal, del_principal)

    def has_route_args(self, *args):
        for name in args:
            if name not in self.route_args or self.route_args[name] is None:
                return False
        return True
