#coding=utf-8
'''
Created on 2013-4-5

@author: fengclient
'''
import json
from gearman import DataEncoder

class JSONDataEncoder(DataEncoder):
    @classmethod
    def encode(cls, encodable_object):
        return json.dumps(encodable_object)

    @classmethod
    def decode(cls, decodable_string):
        return json.loads(decodable_string)

def md5sum(s):
    import hashlib
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()
