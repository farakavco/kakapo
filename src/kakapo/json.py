# -*- coding: utf-8 -*-
#import json
import simplejson as json
__author__ = 'vahid'


def _json_default(o):
    if hasattr(o, 'to_json'):
        return o.to_json()
    return o


def loads(o, *args, **kwargs):
    return json.loads(o, *args, **kwargs)


def dumps(o, *args, **kw):
    return json.dumps(o, default=_json_default, *args, **kw)
