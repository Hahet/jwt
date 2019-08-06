import hmac
import json
import base64
import hashlib


class JWT(object):

    def __init__(self, key):
        self.key = key

    @staticmethod
    def base64url_encode(input: bytes):
        r = base64.urlsafe_b64encode(input)
        # 返回时要把base64编码结尾的=号去除掉
        return r.replace(b'=', b'')

    @staticmethod
    def base64url_decode(input: bytes):
        # 解码时要把base64的结尾=号补齐, base64以4为一个单元
        l = len(input)
        y = (l % 4) * b'='
        input += y
        return base64.urlsafe_b64decode(input)

    def encode(self, header, payload):
        h = str.encode(self.dumps(header))
        p = str.encode(self.dumps(payload))
        a = self.base64url_encode(h) + b'.' + self.base64url_encode(p)
        sign = self.signature(a)
        jwt = a + b'.' + sign
        return jwt

    def validate(self, header_payload, signature):
        v = self.signature(header_payload)
        return v == signature

    def decode(self, jwt_bytes):
        j = jwt_bytes.split(b'.')
        header, payload, signature = j
        v = self.validate(header + b'.' + payload, signature)
        data = {}
        if v:
            h = self.base64url_decode(header)
            p = self.base64url_decode(payload)
            data = {
                'header': h,
                'payload': p
            }
        return v, data

    def signature(self, input):
        # 对前Header.Payload进行签名, 使用Hmac sha256
        sign = hmac.new(self.key, input, digestmod=hashlib.sha256)
        return self.base64url_encode(sign.digest())

    def dumps(self, dt):
        return json.dumps(dt, separators=(',', ':'), ensure_ascii=False)

    def load(self, dt):
        return json.loads(dt)
