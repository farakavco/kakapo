# -*- coding: utf-8 -*-
#import json
import rapidjson as json


def loads(o, *args, **kwargs):
    return json.loads(o, *args, **kwargs)


def dumps(o, *args, **kw):
    return json.dumps(o, default=lambda x: x.to_json())
