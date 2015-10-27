# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from django.conf import settings
from json import JSONEncoder


def print_debug(message):
    if settings.DEBUG:
        print message
    else:
        pass


class StrJSONEncoder(JSONEncoder):
    def default(self, obj):
        for o in obj:
            for k, v in o.iteritems():
                t = k
                if k.find('__') != -1:
                    del o[t]
                    t = k.split('__')[0]
                o[t] = str(v)
        return list(obj)

