# From O'Reilly Python Cookbook
# http://chimera.labs.oreilly.com/books/1230000000393/ch06.html

import json

# strip('[]') if retrieving from API
s = '{"name": "ACME", "shares": 50, "price": 490.1}'

class JSONObject:
    def __init__(self, d):
        self.__dict__ = d

def json_to_obj(t):
    return json.loads(t, object_hook=JSONObject)

data = json_to_obj(s)
data.name
data.shares
data.price

def ordered_dict_example():
    from collections import OrderedDict
    data = json.loads(s, object_pairs_hook=OrderedDict)
    data
