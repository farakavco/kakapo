# -*- coding: utf-8 -*-
import mimetypes
import os.path
from wheezy.http import HTTPResponse
from wheezy.web.handlers.method import MethodHandler
__author__ = 'vahid'


HTTP_HEADER_ACCEPT_RANGE_NONE = ('Accept-Ranges', 'none')


def single_file_handler(filepath):
    abspath = os.path.abspath(filepath)
    assert os.path.exists(abspath)
    assert os.path.isfile(abspath)
    return lambda request: SingleFileHandler(
        request,
        filepath=abspath)


class SingleFileHandler(MethodHandler):

    def __init__(self, request, filepath):
        self.filepath = filepath
        super(SingleFileHandler, self).__init__(request)

    def head(self):
        return self.get(skip_body=True)

    def get(self, skip_body=False):

        mime_type, encoding = mimetypes.guess_type(self.filepath)
        response = HTTPResponse(mime_type or 'plain/text', encoding)
        if not skip_body:
            response.headers.append(HTTP_HEADER_ACCEPT_RANGE_NONE)
            file = open(self.filepath, 'rb')
            try:
                response.write_bytes(file.read())
            finally:
                file.close()
        return response
